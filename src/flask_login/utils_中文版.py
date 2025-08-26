import hmac
from functools import wraps
from hashlib import sha512
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlsplit
from urllib.parse import urlunsplit

from flask import current_app
from flask import g
from flask import has_request_context   # has_request_context() 是 Flask 提供的一个实用函数 (Utility Function)，用于检查当前是否处于一个
                                            # 有效的请求上下文 (Request Context) 中。
                                        #  总结
                                            # has_request_context() 是一个检查函数，用于判断当前代码执行环境是否处于一个活动的 HTTP 请求处理流程中。
                                            # 核心目的: 避免在没有请求上下文时直接访问 request 或 session 而导致 RuntimeError。
                                            # 典型用法: 在编写可能被用在不同上下文（如视图函数、CLI 命令、后台任务、工具函数）中的代码时，进行安全检查。
                                            # 相关函数: has_app_context() (检查应用上下文), request_ctx (底层的请求上下文对象)。
                                            # 简单来说，在你打算使用 request 或 session 之前，如果不确定上下文，最好先用 has_request_context() 问一句：“现在方便吗？”
from flask import request
from flask import session
from flask import url_for
from werkzeug.local import LocalProxy

from .config import COOKIE_NAME
from .config import EXEMPT_METHODS
from .signals import user_logged_in
from .signals import user_logged_out
from .signals import user_login_confirmed


#: 当前用户的代理对象。如果没有用户登录，这将是一个匿名用户对象。
current_user = LocalProxy(lambda: _get_user())
        # 解决上下文依赖问题：在 Web 应用中，像 request、current_app 这样的对象是每个请求都不同的。
        # LocalProxy 允许你定义一个全局变量（如 from flask import request），但在不同的请求上下文中，这个变量会自动指向当前请求的 Request 对象。

def encode_cookie(payload, key=None):
    """
    此函数将一个 ``str`` 类型的值编码成一个 Cookie，并使用应用的密钥（secret key）对该 Cookie 进行签名。

    :param payload: 要编码的值，类型为 `str`。
    :type payload: str

    :param key: 用于创建 Cookie 摘要（digest）的密钥。如果未指定，则使用应用配置中的 SECRET_KEY 值。
    :type key: str
    """
    # 将原始数据和其摘要（通过 HMAC 算法生成）用竖线 "|" 连接起来，形成最终的 Cookie 值。
    return f"{payload}|{_cookie_digest(payload, key=key)}"


def decode_cookie(cookie, key=None):
    """
    此函数解码由 `encode_cookie` 生成的 Cookie。如果 Cookie 的验证失败，将隐式返回 ``None``。

    :param cookie: 一个已编码的 Cookie 字符串。
    :type cookie: str

    :param key: 用于创建 Cookie 摘要的密钥。如果未指定，则使用应用配置中的 SECRET_KEY 值。
    :type key: str
    """
    try:
        # 将 Cookie 字符串按最后一个 "|" 分割，得到原始数据 (payload) 和摘要 (digest)
        payload, digest = cookie.rsplit("|", 1)
        # 如果 digest 是 bytes 类型（在某些 Python 版本下可能），则解码为 ASCII 字符串。
        # pragma: no cover 表示此行在标准测试中通常不会被执行到。
        if hasattr(digest, "decode"):
            digest = digest.decode("ascii")  # pragma: no cover
    except ValueError:
        # 如果分割失败（例如，Cookie 格式错误或没有 "|"），则返回 None。
        return

    # 使用相同的密钥和算法重新计算 payload 的摘要，并与传入的 digest 进行安全比较。
    # 使用 hmac.compare_digest 可以防止时序攻击（timing attack）。
    if hmac.compare_digest(_cookie_digest(payload, key=key), digest):
        # 如果摘要匹配，则验证通过，返回原始的 payload（即用户 ID）。
        return payload
    # 如果摘要不匹配，函数自然结束，返回 None。


def make_next_param(login_url, current_url):
    """
    减少给定 URL 的 scheme（协议）和 host（主机）部分，以便更高效地将其作为参数传递给给定的 `login` URL。
    这可以避免在 `next` 参数中存储完整的绝对 URL，从而减少长度并提高安全性（防止重定向到外部站点）。

    :param login_url: 正在重定向到的登录 URL。
    :type login_url: str
    :param current_url: 需要被简化的 URL。
    :type current_url: str
    
    
    例子1：
        login_url = "https://shop.com/login"
        current_url = "https://shop.com/cart?ref=header#items"

        # 解析
        l_url = urlsplit(login_url) 
        # -> SplitResult(scheme='https', netloc='shop.com', path='/login', query='', fragment='')
        c_url = urlsplit(current_url)
        # -> SplitResult(scheme='https', netloc='shop.com', path='/cart', query='ref=header', fragment='items')

        # 检查条件
        # l_url.scheme ('https') == c_url.scheme ('https') -> True
        # l_url.netloc ('shop.com') == c_url.netloc ('shop.com') -> True
        # 条件满足，进行简化

        simplified_next = urlunsplit(("", "", "/cart", "ref=header", ""))
        # -> "/cart?ref=header" (注意：fragment '#' 通常不包含在 next 参数中，因为它是客户端处理的)

        print(simplified_next) # 输出: "/cart?ref=header"
        
   
    例子2：
        login_url = "/login" # 相对路径，scheme 和 netloc 为空
        current_url = "https://shop.com/profile?edit=true"

        # 解析
        l_url = urlsplit(login_url)
        # -> SplitResult(scheme='', netloc='', path='/login', query='', fragment='')
        c_url = urlsplit(current_url)
        # -> SplitResult(scheme='https', netloc='shop.com', path='/profile', query='edit=true', fragment='')

        # 检查条件
        # not l_url.scheme -> True (因为 l_url.scheme 是空字符串)
        # not l_url.netloc -> True (因为 l_url.netloc 是空字符串)
        # 由于 `not l_url.scheme` 为 True，第一个 `and` 条件成立；`not l_url.netloc` 为 True，第二个 `and` 条件也成立。
        # 条件满足，进行简化

        simplified_next = urlunsplit(("", "", "/profile", "edit=true", ""))
        # -> "/profile?edit=true"

        print(simplified_next) # 输出: "/profile?edit=true"
    
    
    总结：
        make_next_param 函数是一个预防性措施：
            主要目的：在安全的前提下，尽量缩短 next 参数，使其更像一个相对路径。
            安全边界：它通过比较 login_url 和 current_url 的 scheme 和 netloc 来判断是否“同域”。只有同域才允许简化。
            不是最终防线：它不能完全防止开放重定向攻击。最终的、最重要的安全检查必须在服务器端处理 next 参数时进行，
                        即验证 next 参数（无论是简化后的还是完整的）是否指向一个可信的、内部的 URL。make_next_param 
                        只是让这个验证过程更高效（处理短路径比处理长 URL 简单），并减少了暴露完整外部 URL 的风险。
    """
    # 解析 login_url 和 current_url
    l_url = urlsplit(login_url)
    c_url = urlsplit(current_url)

    # 如果 current_url 的协议和主机与 login_url 相同（或 login_url 未指定协议/主机），
    # 则可以安全地只传递路径、查询和片段部分。
    if (not l_url.scheme or l_url.scheme == c_url.scheme) and (
        not l_url.netloc or l_url.netloc == c_url.netloc
    ):
        # 重新组合一个仅包含路径、查询和片段的 URL（scheme 和 netloc 为空）。
        return urlunsplit(("", "", c_url.path, c_url.query, ""))
    # 如果协议或主机不同，则必须返回完整的 current_url，以确保重定向正确。
    return current_url


def expand_login_view(login_view):
    """
    返回登录视图的 URL。如果需要，会将视图名称（view name）扩展为实际的 URL。

    :param login_view: 登录视图的名称，或登录视图的实际 URL。
    :type login_view: str
    """
    # 如果 login_view 已经是一个绝对 URL（以 http://, https://, / 开头），则直接返回。
    if login_view.startswith(("https://", "http://", "/")): # startswith：方法是 Python 字符串对象的一个内置方法，用于检查字符串是否以特定的前缀开始。
        return login_view

    # 否则，假设它是一个视图函数名称，使用 Flask 的 url_for 函数将其转换为 URL。
    return url_for(login_view)


def login_url(login_view, next_url=None, next_field="next"):
    """
    创建一个用于重定向到登录页面的 URL。
    如果只提供了 `login_view`，则此函数仅返回该视图的 URL。
    但如果提供了 `next_url`，则此函数会将一个 ``next=URL`` 参数附加到查询字符串中，
    以便登录视图可以将用户重定向回该 URL。
    Flask-Login 的默认未授权处理程序在重定向到你的登录 URL 时会使用此函数。

    为了强制使用特定的主机名进行重定向，请将 `FORCE_HOST_FOR_REDIRECTS` 配置为一个主机名。
    这可以防止在 `SERVER_NAME` 未配置时重定向到外部站点。

    :param login_view: 登录视图的名称。（或者，登录视图的实际 URL。）
    :type login_view: str
    :param next_url: 提供给登录视图用于重定向的 URL。
    :type next_url: str
    :param next_field: 在查询字符串中存储下一个 URL 的字段名。（默认为 ``next``。）
    :type next_field: str
    """
    # 首先，将 login_view（可能是视图名）扩展为实际的 URL。
    base = expand_login_view(login_view)

    # 如果没有指定 next_url，则直接返回基础登录 URL。
    if next_url is None:
        return base

    # 解析基础 URL
    parsed_result = urlsplit(base)  # urlsplit 函数是Python标准库中的一个模块，位于urllib.parse中。它将给定的URL字符串解析为一个namedtuple对象，
                                            # 并返回五个组成URL的部分，分别是scheme、netloc、path、query和fragment。
    # 解析基础 URL 的查询字符串，得到一个字典（保留空值）
    md = parse_qs(parsed_result.query, keep_blank_values=True)
    
    # 使用 make_next_param 处理 next_url，生成一个可能被简化的 next 参数值。
    md[next_field] = make_next_param(base, next_url)
    
    # 确定重定向的目标主机名。
    # 优先使用 FORCE_HOST_FOR_REDIRECTS 配置，如果未配置，则使用原始 URL 的主机名。
    netloc = current_app.config.get("FORCE_HOST_FOR_REDIRECTS") or parsed_result.netloc
    
    # 使用新的查询字符串和（可能修改的）主机名创建一个新的 URL 元组。
    # 其中，scheme 和 path 保持不变，query 使用 urlencode 将参数字典编码为查询字符串。
            # urlencode功能：URL 编码确保所有浏览器都能正确传输 URL 字符串中的文本。 问号 ( ) 、和号 (&) 、斜杠标记 (/) 等字符，
                            # 某些浏览器可能会截断或损坏空格。 因此，必须在标记或查询字符串中 <a> 对这些字符进行编码，浏览器可以
                            # 在请求字符串中重新发送字符串。
    parsed_result = parsed_result._replace(
        netloc=netloc, query=urlencode(md, doseq=True)
    )
    
    # 将元组重新组合成最终的 URL 字符串并返回。
    return urlunsplit(parsed_result)


def login_fresh():
    """
    如果当前登录是“新鲜的”（即通过显式登录操作获得，而非通过“记住我”Cookie 恢复），则返回 ``True``。
    """
    # 检查会话中 _fresh 标记的值，如果不存在则默认为 False。
    return session.get("_fresh", False)


def login_remembered():
    """
    如果当前登录是跨会话“被记住的”（即通过“记住我”Cookie 恢复的登录状态），则返回 ``True``。
    """
    # 获取应用配置
    config = current_app.config
    # 获取“记住我”Cookie 的名称
    cookie_name = config.get("REMEMBER_COOKIE_NAME", COOKIE_NAME)   # current_app.config 是 Flask 提供的一个接口，用于访问当前应用的配置。
                                                                    # 这里的 config 通常指的是一个 字典（dict） 或一个 类似字典的对象，
                                                                        # 它存储了应用程序的所有配置项。
                                                                    # .get方法：这是 Python 字典对象的一个内置方法，用于从字典中获取指定键的值。
                                                                    # 即： config.get("REMEMBER_COOKIE_NAME", COOKIE_NAME) 是从 config 字典
                                                                        # 中获取键 "REMEMBER_COOKIE_NAME" 对应的值。
                                                                        # 如果该键不存在，则返回默认值 COOKIE_NAME。    
    # 检查请求中是否存在该 Cookie，且会话中的 _remember 标记不是 'clear'
    has_cookie = cookie_name in request.cookies and session.get("_remember") != "clear" # 执行顺序：先判断 cookie_name 是否在 request.cookies 中，
                                                                                                 # 再判断 session.get("_remember") != "clear"
                                                                                                 # 然后将两个判断值进行与运算，
                                                                                                 # 最后将判断结果，即布尔值赋值给 has_cookie 变量。  
    # 如果存在有效的“记住我”Cookie
    if has_cookie:
        # 获取 Cookie 值
        cookie = request.cookies[cookie_name]
        # 尝试解码 Cookie 获取用户 ID
        user_id = decode_cookie(cookie)
        # 如果成功解码出用户 ID，则说明是通过 Cookie 登录的。
        return user_id is not None
    # 如果没有有效的 Cookie，则不是“被记住”的登录。
    return False


def login_user(user, remember=False, duration=None, force=False, fresh=True):
    """
    登录一个用户。你应该将实际的用户对象传递给此函数。
    如果用户的 `is_active` 属性为 ``False``，除非 `force` 参数为 ``True``，否则他们将无法登录。

    如果登录尝试成功，此函数将返回 ``True``；如果失败（例如，因为用户处于非活动状态），则返回 ``False``。

    :param user: 要登录的用户对象。
    :type user: object
    :param remember: 用户会话过期后是否记住该用户。默认为 ``False``。
    :type remember: bool
    :param duration: “记住我”Cookie 的有效期。如果为 ``None``，则使用配置中的值。默认为 ``None``。
    :type duration: :class:`datetime.timedelta`
    :param force: 如果用户处于非活动状态，将此参数设置为 ``True`` 将无视此状态并登录用户。默认为 ``False``。
    :type force: bool
    :param fresh: 将此参数设置为 ``False`` 将以标记为“不新鲜”（not "fresh"）的会话登录用户。默认为 ``True``。
    :type fresh: bool
    """
    # 如果不是强制登录，且用户不活跃（is_active 为 False），则登录失败，返回 False。
    if not force and not user.is_active:
        return False

    # 获取用户的唯一标识符（ID）。使用 login_manager 配置的 id_attribute 方法（默认是 'get_id'）。
    # 整体意思: 动态地获取 user 对象上名为 get_id（或由 id_attribute 指定的其他名字）的方法，并立即调用它，将其返回值赋给 user_id。
    user_id = getattr(user, current_app.login_manager.id_attribute)()  
            # getattr() 是 Python 的内置函数 (Built-in Function)。可以在任何 Python 环境中直接使用它，无需 import
                #作用: getattr(object, name[, default]) 用于获取一个对象的属性值。
                    # object: 要获取属性的对象。
                    # name: 要获取的属性名（字符串）。
                    # default (可选): 如果属性不存在时返回的默认值。如果未提供且属性不存在，则抛出 AttributeError。
            # 此处 getattr(...)() 有两个括号，第一个括号返回的是 getattr(...) 函数的执行结果，而这个结果是 "get_id" 这个函数，
                                         # 那第二个括号就代表着：“get_id” + “()” ， 即：返回这个 get_id() 函数的执行结果，最后赋值给 user_id 。 
            # 代码使用 getattr(user, current_app.login_manager.id_attribute) 而不是直接写 user.get_id() 的原因是灵活性和可配置性。
                # id_attribute 是一个可配置的属性。默认是 "get_id"，但开发者可以将其改为其他名字，比如 "get_user_id" 或 "id"。
                # 通过 getattr()，Flask-Login 可以动态地根据 id_attribute 的值去查找用户对象上的对应方法。
                # 这样，Flask-Login 就不强制要求用户对象必须有一个叫 get_id 的方法，只要有一个名字由 id_attribute 指定的、能返回用户 ID 的方法即可。

    # 将用户 ID 存入会话
    session["_user_id"] = user_id
    # 标记会话是否“新鲜”
    session["_fresh"] = fresh
    # 生成并存储当前会话的唯一标识符，用于会话保护
    session["_id"] = current_app.login_manager._session_identifier_generator()

    # 如果需要“记住我”功能
    if remember:
        # 在会话中设置标记，指示在响应时需要设置“记住我”Cookie
        session["_remember"] = "set"
        # 如果指定了自定义的有效期
        if duration is not None:
            try:
                # 将 timedelta 对象转换为总秒数（浮点数）。
                # 这种写法兼容 Python 2.6（因为 total_seconds() 在 2.7 才引入）。
                session["_remember_seconds"] = (
                    duration.microseconds
                    + (duration.seconds + duration.days * 24 * 3600) * 10**6
                ) / 10.0**6
            except AttributeError as e:
                # 如果 duration 不是 timedelta 对象，则抛出异常。
                raise Exception(
                    f"duration 必须是一个 datetime.timedelta 对象，但实际得到的是: {duration}"
                ) from e

    # 更新请求上下文中的用户对象（g._login_user），使其立即可用。
    current_app.login_manager._update_request_context_with_user(user)
    # 发送用户已登录的信号。
    user_logged_in.send(current_app._get_current_object(), user=_get_user())
    # 登录成功，返回 True。
    return True


def logout_user():
    """
    注销当前登录的用户。（您不需要传入实际的用户对象。）此函数还会清理“记住我”Cookie（如果存在的话）。
    """

    # 获取当前用户对象（用于发送信号）
    user = _get_user()

    # 从会话中移除用户 ID
    if "_user_id" in session:
        session.pop("_user_id")

    # 从会话中移除“新鲜度”标记
    if "_fresh" in session:
        session.pop("_fresh")

    # 从会话中移除会话 ID 标记
    if "_id" in session:
        session.pop("_id")

    # 获取“记住我”Cookie 的名称
    cookie_name = current_app.config.get("REMEMBER_COOKIE_NAME", COOKIE_NAME)
    # 检查请求中是否存在该 Cookie
    if cookie_name in request.cookies:
        # 在会话中设置标记，指示在响应时需要清除“记住我”Cookie
        session["_remember"] = "clear"
        # 如果会话中存在“记住我”的过期时间设置，也一并清除
        if "_remember_seconds" in session:
            session.pop("_remember_seconds")

    # 发送用户已注销的信号。
    user_logged_out.send(current_app._get_current_object(), user=user)

    # 更新请求上下文中的用户对象为 None（匿名用户）。
    current_app.login_manager._update_request_context_with_user()
    # 注销成功，返回 True。
    return True


def confirm_login():
    """
    此函数将当前会话标记为“新鲜的”。当会话从“记住我”Cookie 中恢复时，会变得“陈旧”（stale）。
    调用此函数可以确认用户刚刚重新登录（例如，在一个需要重新输入密码的敏感操作后），从而使其会话重新变为“新鲜”。
    """
    # 将会话的“新鲜度”标记设置为 True。
    session["_fresh"] = True
    # 生成一个新的会话标识符，以增强安全性。
    session["_id"] = current_app.login_manager._session_identifier_generator()
    # 发送用户登录已确认的信号。
    user_login_confirmed.send(current_app._get_current_object())


def login_required(func):
    """
    如果你用这个装饰器修饰一个视图函数，它将确保在调用实际的视图函数之前，当前用户已经登录并经过身份验证。
    （如果用户未登录，它将调用 :attr:`LoginManager.unauthorized` 回调函数。）例如::

        @app.route('/post')
        @login_required
        def post():
            pass

    如果你只在某些特定情况下需要要求用户登录，你可以这样做::

        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()

    ...这本质上就是此装饰器添加到你视图函数中的代码。

    .. 注意 ::

        根据 `W3 关于 CORS 预检请求的指南
        <http://www.w3.org/TR/cors/#cross-origin-request-with-preflight-0>`_，
        HTTP ``OPTIONS`` 请求被豁免于登录检查。

    :param func: 要修饰的视图函数。
    :type func: function
    """

    # 使用 wraps 保持被装饰函数的元数据（如 __name__, __doc__）
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # 如果请求方法在豁免列表中（如 'OPTIONS'），则直接放行。
        if request.method in EXEMPT_METHODS:
            pass
        # 否则，如果用户未认证，则调用未授权处理程序。
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()

        # flask 1.x 兼容性
        # current_app.ensure_sync 仅在 Flask >= 2.0 中可用
        # 对于 Flask 2.0+，使用 ensure_sync 确保异步视图能被正确调用。
        if callable(getattr(current_app, "ensure_sync", None)):
            return current_app.ensure_sync(func)(*args, **kwargs)
        # 对于 Flask 1.x，直接调用原函数。
        return func(*args, **kwargs)

    # 返回装饰后的视图函数。
    return decorated_view


def fresh_login_required(func):
    """
    如果你用这个装饰器修饰一个视图函数，它将确保当前用户的登录是“新鲜的”——即，他们的会话不是从“记住我”Cookie 恢复的。
    敏感操作，比如更改密码或电子邮件，应该用此装饰器保护，以阻碍 Cookie 窃取者的努力。

    如果用户未认证，:meth:`LoginManager.unauthorized` 会像往常一样被调用。如果用户已认证，但其会话不是“新鲜的”，
    则会调用 :meth:`LoginManager.needs_refresh` 方法。（在这种情况下，你需要提供一个 :attr:`LoginManager.refresh_view` 来处理刷新请求。）

    在配置变量方面，此装饰器的行为与 :func:`login_required` 装饰器完全相同。

    .. 注意 ::

        根据 `W3 关于 CORS 预检请求的指南
        <http://www.w3.org/TR/cors/#cross-origin-request-with-preflight-0>`_，
        HTTP ``OPTIONS`` 请求被豁免于登录检查。

    :param func: 要修饰的视图函数。
    :type func: function
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        # 如果请求方法在豁免列表中（如 'OPTIONS'），则直接放行。
        if request.method in EXEMPT_METHODS:
            pass
        # 如果用户未认证，则调用未授权处理程序。
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        # 如果用户已认证但会话不新鲜，则调用需要刷新的处理程序。
        elif not login_fresh():
            return current_app.login_manager.needs_refresh()
        try:
            # current_app.ensure_sync 在 Flask >= 2.0 中可用
            # 对于 Flask 2.0+，使用 ensure_sync 确保异步视图能被正确调用。
            return current_app.ensure_sync(func)(*args, **kwargs)
        except AttributeError:  # pragma: no cover
            # 对于 Flask 1.x，直接调用原函数。
            return func(*args, **kwargs)

    # 返回装饰后的视图函数。
    return decorated_view


def set_login_view(login_view, blueprint=None):
    """
    为应用或蓝图设置登录视图。如果传递了蓝图，则登录视图会被设置在 ``blueprint_login_views`` 字典中，键为蓝图名称。

    :param login_view: 登录视图的名称或 URL。 (原文此处有误，应为登录视图，而非用户对象)
    :type login_view: str
    :param blueprint: 应设置此登录视图的蓝图。默认为 ``None``。
    :type blueprint: object
    """
    # 获取当前应用中已注册的蓝图登录视图的数量
    num_login_views = len(current_app.login_manager.blueprint_login_views)
    # 如果指定了蓝图，或者已经为其他蓝图设置了登录视图
    if blueprint is not None or num_login_views != 0:
        # 将指定的登录视图存储到蓝图登录视图字典中，键为蓝图的名称
        (current_app.login_manager.blueprint_login_views[blueprint.name]) = login_view

        # 如果全局的 login_view 已经被设置，并且 None 键（代表全局）尚未在蓝图字典中，
        # 则将全局 login_view 也存入蓝图字典中，键为 None。
        # 这是为了在有蓝图视图时，也能保留全局视图的引用。
        if (
            current_app.login_manager.login_view is not None
            and None not in current_app.login_manager.blueprint_login_views
        ):
            (
                current_app.login_manager.blueprint_login_views[None]
            ) = current_app.login_manager.login_view

        # 一旦开始使用蓝图级别的登录视图，就将全局 login_view 置为 None。
        # 这会触发 LoginManager 使用蓝图字典来查找登录视图。
        current_app.login_manager.login_view = None
    else:
        # 如果没有使用蓝图，或者这是第一个设置，则直接设置全局 login_view。
        current_app.login_manager.login_view = login_view


def _get_user():
    """
    内部函数：获取当前请求上下文中的用户对象。
    """
    # 检查是否处于请求上下文中
    if has_request_context():
        # 如果 g._login_user 不存在，则调用 _load_user 方法加载用户
        if "_login_user" not in g:
            current_app.login_manager._load_user()

        # 返回存储在 g 对象中的当前用户
        return g._login_user

    # 如果不在请求上下文中，返回 None
    return None


def _cookie_digest(payload, key=None):
    """
    内部函数：为给定的 payload 生成一个 HMAC 摘要（digest）。
    """
    # 获取用于签名的密钥
    key = _secret_key(key)
    # 使用 SHA512 算法和密钥对 payload（编码为 UTF-8 bytes）进行 HMAC 运算，并返回十六进制字符串形式的摘要。
    return hmac.new(key, payload.encode("utf-8"), sha512).hexdigest()


def _create_identifier():
    """
    内部函数：为当前会话创建一个唯一的标识符（ID）。
    基于客户端的 IP 地址和用户代理字符串生成一个 SHA512 哈希值。
    """
    # 创建一个 SHA512 哈希对象
    h = sha512()
    # 将客户端的远程地址 (IP) 和用户代理字符串组合起来，并编码后更新到哈希对象中。
    h.update(f"{request.remote_addr}|{request.user_agent.string}".encode())
    # 返回哈希值的十六进制字符串。
    return h.hexdigest()


def _user_context_processor():
    """
    内部函数：上下文处理器，用于将 current_user 变量注入到所有模板的上下文中。
    """
    # 返回一个字典，其中 'current_user' 的值是通过 _get_user() 获取的当前用户。
    return dict(current_user=_get_user())


def _secret_key(key=None):
    """
    内部函数：获取应用的密钥（secret key）。如果传入了 key，则使用传入的 key；
    否则，从应用配置中获取 SECRET_KEY。
    如果密钥是字符串类型，则将其编码为字节（bytes）。
    """
    if key is None:
        key = current_app.config["SECRET_KEY"]

    # 如果密钥是字符串，则编码为 latin1 字节（确保是 bytes 类型）。
    # pragma: no cover 表示此行在标准测试中可能不会被执行到（因为 SECRET_KEY 通常直接配置为 bytes）。
    if isinstance(key, str):  # pragma: no cover
        key = key.encode("latin1")  # ensure bytes

    return key