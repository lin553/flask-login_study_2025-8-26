from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import abort         # 作用：立即终止当前请求的处理，并返回一个指定的 HTTP 错误状态码给客户端。 调用 abort() 后，函数后续代码不会执行。
                                    # 它会触发你用 @app.errorhandler() 定义的错误处理函数。
from flask import current_app   # 作用：获取当前激活的 Flask 应用实例。它允许你在应用上下文中访问应用的配置、路由等属性，而无需显式传递应用对象。
                                    # 即： 创建 Flask 应用实例：    app = Flask(__name__)
                                # 用途：一旦应用上下文存在，current_app 就可以安全地访问该 Flask 实例的所有属性和方法，例如：
                                    # current_app.config: 应用的配置字典。
                                    # current_app.logger: 应用的日志记录器。
                                    # current_app.extensions: 所有已注册的 Flask 扩展。
                                    # current_app.url_map: 应用的 URL 路由映射。
                                    # current_app.test_client(): 获取测试客户端。
                                    # 以及任何你在 app 实例上定义的自定义属性或方法。
                                # 总结 current_app 的范围：“当前”指的是在由特定 Flask 应用实例的请求、CLI 命令或手动 app_context() 块所激活的应
                                    # 用上下文生命周期内。它提供了一种全局、便捷且线程安全的方式来访问那个特定的 app 对象。
from flask import flash         # 作用：将一条消息存储在会话中，以便在下一个请求中显示给用户。通常用于向用户显示一次性的通知或提示信息。
                                    # 它利用 session 作为临时存储，是实现用户友好反馈（特别是配合 PRG 模式）的关键工具。
from flask import g             # 作用：提供一个用于存储请求级别数据的命名空间对象。你可以将数据存储在 g 对象上，并在同一请求的不同函数中访问这些数据。
                                    # g 对象在每次请求开始时被创建，在请求结束时被销毁。它非常适合存储在请求处理过程中需要被多个函数共享的数据，比如数据库连接、
                                    # 当前登录的用户对象（在某些认证实现中）、解析后的请求数据等。注意：g 是请求级别的，不同请求之间的 g 对象是隔离的。
                                # 目的：为单个 HTTP 请求的处理过程提供一个共享的、临时的命名空间。它允许你在请求处理链中的不同函数（如 before_request 处理器、
                                    # 视图函数、辅助函数）之间传递数据，而无需通过函数参数层层传递。
                                # 总结 g：g 是 Flask 提供的一个轻量级、请求级别的“便签本”或“临时仓库”。它极大地简化了在单个请求处理流程中共享数据和状态的复杂性，
                                    # 是提高代码效率和可读性的重要工具，但其作用范围严格限定在单个 HTTP 请求的生命周期内。
from flask import redirect      # 作用：生成一个 HTTP 302 重定向响应，将用户浏览器重定向到另一个 URL。通常用于在处理完某个请求后，指示浏览器跳转到另一个页面。
                                    # 以防止用户刷新页面时重复提交表单。也用于登录/登出后的跳转。
from flask import request       # 作用：提供对当前请求的访问。它是一个全局对象，包含了请求的所有信息，如请求方法（GET/POST）、URL、查询参数、表单数据、头信息等。
                                # 用途：这是获取客户端数据的主要方式。你可以通过它访问：
                                    # request.args：URL 查询参数 (e.g., ?key=value)。
                                    # request.form：表单数据（来自 POST/PUT 请求的 body）。
                                    # request.values：合并了 args 和 form。
                                    # request.cookies：请求中的 Cookie。
                                    # request.headers：HTTP 请求头。
                                    # request.method：请求方法 (GET, POST, PUT, DELETE 等)。
                                    # request.url：完整的请求 URL。
                                    # request.json：解析后的 JSON 数据（如果 Content-Type 是 application/json）。
from flask import session       # 作用：提供对当前会话的访问。它是一个全局对象，用于存储用户会话数据，如登录状态、用户偏好设置等。
                                    # session 是 Flask 中用于在用户的不同 HTTP 请求之间保持状态的机制。HTTP 本身是无状态的，
                                    # session 提供了有状态的用户体验基础（如登录状态）。
                                # 用途：实现“有状态”的会话。最典型的用途是保持用户登录状态（存储用户 ID）。Flask 的 session 默认是签名 Cookie，这意味着数据存储在客户端的浏览器 Cookie 中，
                                    # 但经过加密签名以防止篡改。服务器不存储 session 数据（除非你配置了服务器端 session）




from .config import COOKIE_DURATION
from .config import COOKIE_HTTPONLY
from .config import COOKIE_NAME
from .config import COOKIE_SAMESITE
from .config import COOKIE_SECURE
from .config import ID_ATTRIBUTE
from .config import LOGIN_MESSAGE
from .config import LOGIN_MESSAGE_CATEGORY
from .config import REFRESH_MESSAGE
from .config import REFRESH_MESSAGE_CATEGORY
from .config import SESSION_KEYS
from .config import USE_SESSION_FOR_NEXT
from .mixins import AnonymousUserMixin
from .signals import session_protected
from .signals import user_accessed
from .signals import user_loaded_from_cookie
from .signals import user_loaded_from_request
from .signals import user_needs_refresh
from .signals import user_unauthorized
from .utils import _create_identifier
from .utils import _user_context_processor
from .utils import decode_cookie
from .utils import encode_cookie
from .utils import expand_login_view
from .utils import login_url as make_login_url
from .utils import make_next_param

class LoginManager:
    """该对象用于保存登录相关的配置设置。
    :class:`LoginManager` 的实例*不*与特定的应用（app）绑定，
    因此你可以在代码的主模块中创建一个实例，
    然后在工厂函数中将其绑定到你的应用上。
    """

    def __init__(self, app=None, add_context_processor=True):
        #: 一个类或工厂函数，用于生成匿名用户对象。
        #: 当没有用户登录时，将使用此匿名用户。
        self.anonymous_user = AnonymousUserMixin

        #: 当用户需要登录时，重定向到的视图名称。
        #: （这里也可以是一个绝对 URL，如果你的认证机制在应用外部。）
        self.login_view = None

        #: 按蓝图（Blueprint）划分的、当用户需要登录时重定向到的视图名称。
        #: 如果某个键对应的值为 None，则使用 :attr:`login_view` 的值。
        self.blueprint_login_views = {}

        #: 当用户被重定向到登录页面时，要闪现（flash）给用户的提示消息。
        self.login_message = LOGIN_MESSAGE

        #: 当用户被重定向到登录页面时，要闪现的提示消息的类别（category）。
        self.login_message_category = LOGIN_MESSAGE_CATEGORY

        #: 当用户需要重新认证（reauthenticate）时，重定向到的视图名称。
        self.refresh_view = None

        #: 当用户被重定向到“需要刷新”页面时，要闪现的提示消息。
        self.needs_refresh_message = REFRESH_MESSAGE

        #: 当用户被重定向到“需要刷新”页面时，要闪现的提示消息的类别（category）。
        self.needs_refresh_message_category = REFRESH_MESSAGE_CATEGORY

        #: 会话保护（session protection）使用的模式。
        #: 可以是 ``'basic'``（默认）、``'strong'``，或者 ``None`` 来禁用会话保护。
        self.session_protection = "basic"

        #: 如果存在，用于翻译闪现消息 ``self.login_message`` 和 ``self.needs_refresh_message``。
        self.localize_callback = None

        #: unauthorized 方法使用的回调函数（通过 unauthorized_handler 装饰器注册）。
        self.unauthorized_callback = None

        #: needs_refresh 方法使用的回调函数（通过 needs_refresh_handler 装饰器注册）。
        self.needs_refresh_callback = None

        #: 用于在会话中存储用户 ID 的属性名。
        self.id_attribute = ID_ATTRIBUTE

        #: 用于从会话中加载用户对象的回调函数（通过 user_loader 装饰器注册）。
        self._user_callback = None

        #: 用于从 Flask 请求中加载用户对象的回调函数（通过 request_loader 装饰器注册）。
        self._request_callback = None

        #: 用于生成会话标识符的函数。
        self._session_identifier_generator = _create_identifier

        # 如果在初始化时提供了 app，则立即调用 init_app 进行配置。
        if app is not None:
            self.init_app(app, add_context_processor)

    def init_app(self, app, add_context_processor=True):
        """
        配置一个应用（app）。该方法会注册一个 'after_request' 回调，
        并将此 `LoginManager` 实例作为 `app.login_manager` 附加到应用上。

        :param app: 要配置的 :class:`flask.Flask` 对象。
        :type app: :class:`flask.Flask`
        :param add_context_processor: 是否向应用添加一个上下文处理器（context processor），
            该处理器会将 `current_user` 变量添加到模板中。默认为 ``True``。
        :type add_context_processor: bool
        """
        # 将当前 LoginManager 实例附加到 Flask 应用上，方便后续访问。
        app.login_manager = self
        # 注册一个 after_request 回调，用于处理“记住我”（remember me）功能的 Cookie 更新。
        app.after_request(self._update_remember_cookie)

        # 如果需要，添加上下文处理器，使得在 Jinja2 模板中可以直接使用 current_user。
        if add_context_processor:
            app.context_processor(_user_context_processor)

    def unauthorized(self):
        """
        当用户需要登录才能访问某个资源时，会调用此方法。
        如果你通过 :meth:`LoginManager.unauthorized_handler` 装饰器注册了一个回调函数，
        那么该回调函数将被调用。
        否则，它将执行以下操作：

            - 向用户闪现（flash）:attr:`LoginManager.login_message` 消息。

            - 如果应用使用了蓝图（blueprints），则使用 `blueprint_login_views` 查找当前蓝图的登录视图。
              如果应用没有使用蓝图，或者当前蓝图的登录视图未指定，则使用 `login_view` 的值。

            - 将用户重定向到登录视图。
              （用户试图访问的页面地址将作为 ``next`` 查询字符串参数传递，
              因此登录成功后可以重定向回该页面，而不是首页。
              或者，如果设置了 USE_SESSION_FOR_NEXT，则该地址将作为 ``next`` 存入会话中。）

        如果 :attr:`LoginManager.login_view` 未定义，那么它将直接抛出一个 HTTP 401 (未授权) 错误。

        此方法的返回值应该从视图函数或 before/after_request 函数中返回，
        否则重定向将不会生效。
        """
        # 发送一个信号，通知系统有用户被拒绝访问（未授权）。
        user_unauthorized.send(current_app._get_current_object())

        # 如果用户注册了自定义的未授权处理回调，则调用它并返回其结果。
        if self.unauthorized_callback:
            return self.unauthorized_callback()

        # 确定应该重定向到哪个登录视图。
        # 优先检查当前请求所属的蓝图是否有专用的登录视图。
        if request.blueprint in self.blueprint_login_views:
            login_view = self.blueprint_login_views[request.blueprint]
        else:
            # 否则，使用全局的 login_view。
            login_view = self.login_view

        # 如果最终没有找到任何登录视图，则直接返回 401 未授权错误。
        if not login_view:
            abort(401)

        # 如果设置了登录提示消息，则闪现给用户。
        if self.login_message:
            # 如果设置了本地化（翻译）回调，则先翻译消息。
            if self.localize_callback is not None:
                flash(
                    self.localize_callback(self.login_message),
                    category=self.login_message_category,
                )
            else:
                # 否则直接闪现原始消息。
                flash(self.login_message, category=self.login_message_category)

        # 获取当前应用的配置
        config = current_app.config
        # 检查是否配置使用会话（session）来存储 'next' 参数，而不是放在 URL 查询字符串中。
        # 这通常更安全，可以防止开放重定向攻击。
        if config.get("USE_SESSION_FOR_NEXT", USE_SESSION_FOR_NEXT):
            # 计算登录页面的完整 URL
            login_url = expand_login_view(login_view)
            # 生成一个新的会话 ID（用于 remember me 功能）
            session["_id"] = self._session_identifier_generator()
            # 将用户原本想访问的页面 URL 编码后存入会话
            session["next"] = make_next_param(login_url, request.url)
            # 生成基础的登录 URL（不带 next 参数，因为 next 已存入 session）
            redirect_url = make_login_url(login_view)
        else:
            # 如果不使用会话存储 next，则将目标 URL 作为查询参数附加到登录 URL 上。
            redirect_url = make_login_url(login_view, next_url=request.url)

        # 最终执行 HTTP 302 重定向，跳转到登录页面。
        return redirect(redirect_url)

    def user_loader(self, callback):
        """
        设置从会话中重新加载用户对象的回调函数。
        你设置的函数应该接收一个用户 ID（字符串类型）作为参数，
        并返回一个用户对象，如果用户不存在则返回 ``None``。

        :param callback: 用于检索用户对象的回调函数。
        :type callback: callable
        """
        # 将回调函数保存到实例变量中
        self._user_callback = callback
        # 返回回调函数本身（允许用作装饰器）
        return self.user_callback

    @property
    def user_callback(self):
        """获取通过 user_loader 装饰器设置的 user_loader 回调函数。"""
        return self._user_callback

    def request_loader(self, callback):
        """
        设置从 Flask 请求对象中加载用户对象的回调函数。
        你设置的函数应该接收一个 Flask 请求对象作为参数，
        并返回一个用户对象，如果用户不存在则返回 `None`。

        :param callback: 用于检索用户对象的回调函数。
        :type callback: callable
        """
        # 将回调函数保存到实例变量中
        self._request_callback = callback
        # 返回回调函数本身（允许用作装饰器）
        return self.request_callback

    @property
    def request_callback(self):
        """获取通过 request_loader 装饰器设置的 request_loader 回调函数。"""
        return self._request_callback

    def unauthorized_handler(self, callback):
        """
        设置 `unauthorized` 方法使用的回调函数，
        该函数（除了其他用途外）被 `login_required` 装饰器所使用。
        它不接受任何参数，应该返回一个响应对象，该响应将发送给用户，
        以替代他们原本应该看到的视图。

        :param callback: 用于处理未授权用户的回调函数。
        :type callback: callable
        """
        # 将回调函数保存到实例变量中
        self.unauthorized_callback = callback
        # 返回回调函数本身（允许用作装饰器）
        return callback

    def needs_refresh_handler(self, callback):
        """
        设置 `needs_refresh` 方法使用的回调函数，
        该函数（除了其他用途外）被 `fresh_login_required` 装饰器所使用。
        它不接受任何参数，应该返回一个响应对象，该响应将发送给用户，
        以替代他们原本应该看到的视图。

        :param callback: 用于处理需要刷新认证的用户的回调函数。
        :type callback: callable
        """
        # 将回调函数保存到实例变量中
        self.needs_refresh_callback = callback
        # 返回回调函数本身（允许用作装饰器）
        return callback
    
    def needs_refresh(self):
        """
        当用户已登录，但由于其会话已过期（stale）而需要重新认证（reauthenticate）时，
        会调用此方法。
        如果你通过 `needs_refresh_handler` 装饰器注册了一个回调函数，那么该回调函数将被调用。
        否则，它将执行以下操作：

            - 向用户闪现（flash）:attr:`LoginManager.needs_refresh_message` 消息。

            - 将用户重定向到 :attr:`LoginManager.refresh_view` 指定的视图。
                （用户试图访问的页面地址将作为 ``next`` 查询字符串参数传递，
                因此登录成功后可以重定向回该页面，而不是首页。）

        如果 :attr:`LoginManager.refresh_view` 未定义，那么它将直接抛出一个 HTTP 401 (未授权) 错误。

        此方法的返回值应该从视图函数或 before/after_request 函数中返回，
        否则重定向将不会生效。
        """
        # 发送一个信号，通知系统有用户需要刷新认证。
        user_needs_refresh.send(current_app._get_current_object())

        # 如果用户注册了自定义的“需要刷新”处理回调，则调用它并返回其结果。
        if self.needs_refresh_callback:
            return self.needs_refresh_callback()

        # 如果没有配置 refresh_view，则直接返回 401 未授权错误。
        if not self.refresh_view:
            abort(401)

        # 如果设置了“需要刷新”的提示消息，则闪现给用户。
        if self.needs_refresh_message:
            # 如果设置了本地化（翻译）回调，则先翻译消息。
            if self.localize_callback is not None:
                flash(
                    self.localize_callback(self.needs_refresh_message),
                    category=self.needs_refresh_message_category,
                )
            else:
                # 否则直接闪现原始消息。
                flash(
                    self.needs_refresh_message,
                    category=self.needs_refresh_message_category,
                )

        # 获取当前应用的配置
        config = current_app.config
        # 检查是否配置使用会话（session）来存储 'next' 参数。
        if config.get("USE_SESSION_FOR_NEXT", USE_SESSION_FOR_NEXT):
            # 计算刷新认证页面的完整 URL
            login_url = expand_login_view(self.refresh_view)
            # 生成一个新的会话 ID
            session["_id"] = self._session_identifier_generator()
            # 将用户原本想访问的页面 URL 编码后存入会话
            session["next"] = make_next_param(login_url, request.url)
            # 生成基础的刷新认证 URL（不带 next 参数，因为 next 已存入 session）
            redirect_url = make_login_url(self.refresh_view)
        else:
            # 如果不使用会话存储 next，则将目标 URL 作为查询参数附加到刷新认证 URL 上。
            login_url = self.refresh_view
            redirect_url = make_login_url(login_url, next_url=request.url)

        # 最终执行 HTTP 302 重定向，跳转到刷新认证页面。
        return redirect(redirect_url)

    def _update_request_context_with_user(self, user=None):
        """将给定的用户对象存储到请求上下文（g）中，作为 g._login_user。
        如果未提供用户对象，则创建一个匿名用户实例。
        """
        # 如果没有传入用户，则使用匿名用户类创建一个匿名用户对象。
        if user is None:
            user = self.anonymous_user()

        # 将用户对象存储在 Flask 的 g 对象中，使其在整个请求生命周期内可访问。
        # 这是 Flask-Login 实现 current_user 的核心机制之一。
        g._login_user = user

    def _load_user(self):
        """根据情况从会话（session）或“记住我”（remember_me）Cookie 中加载用户。"""

        # 如果既没有设置 user_loader 回调，也没有设置 request_loader 回调，
        # 则抛出异常，因为无法加载用户。
        if self._user_callback is None and self._request_callback is None:
            raise Exception(
                "缺少 user_loader 或 request_loader 回调。"
                "请参考 http://flask-login.readthedocs.io/#how-it-works 获取更多信息。"
            )

        # 发送一个信号，通知系统用户已被访问（加载）。
        user_accessed.send(current_app._get_current_object())

        # 检查会话保护（Session Protection）是否失败。
        # 如果失败，通常意味着会话可能被劫持，需要降级或清除。
        if self._session_protection_failed():
            # 如果会话保护失败，加载一个匿名用户（或保持当前状态）。
            return self._update_request_context_with_user()

        # 初始化用户对象为 None
        user = None

        # 1. 尝试从 Flask Session 中加载用户
        # 从会话中获取用户 ID
        user_id = session.get("_user_id")
        # 如果会话中有用户 ID 且 user_loader 回调已定义，则调用回调加载用户。
        if user_id is not None and self._user_callback is not None:
            user = self._user_callback(user_id)

        # 2. 如果从会话中没加载到用户，则尝试从“记住我”Cookie 或请求中加载
        if user is None:
            # 获取应用配置
            config = current_app.config
            # 获取“记住我”Cookie 的名称
            cookie_name = config.get("REMEMBER_COOKIE_NAME", COOKIE_NAME)
            # 检查请求中是否存在该 Cookie，且会话中的 _remember 标记不是 'clear'
            has_cookie = (
                cookie_name in request.cookies and session.get("_remember") != "clear"
            )
            # 如果存在有效的“记住我”Cookie
            if has_cookie:
                # 从请求中获取 Cookie 值
                cookie = request.cookies[cookie_name]
                # 尝试从 Cookie 中解析并加载用户
                user = self._load_user_from_remember_cookie(cookie)
            # 如果没有有效的“记住我”Cookie，但定义了 request_loader 回调，
            # 则尝试从当前请求中直接加载用户（例如，API 认证）。
            elif self._request_callback:
                user = self._load_user_from_request(request)

        # 将最终加载到的用户（可能是 None 或具体用户对象）更新到请求上下文中。
        return self._update_request_context_with_user(user)

    def _session_protection_failed(self):
        """检查当前会话是否因会话保护机制而被认为已失效。"""
        # 获取当前会话对象
        sess = session._get_current_object()
        # 生成当前请求的会话标识符
        ident = self._session_identifier_generator()

        # 获取当前应用对象
        app = current_app._get_current_object()
        # 获取会话保护模式（basic, strong, None）
        mode = app.config.get("SESSION_PROTECTION", self.session_protection)

        # 如果未启用会话保护，或者模式无效，则返回 False（未失败）。
        if not mode or mode not in ["basic", "strong"]:
            return False

        # 如果会话为空，说明是匿名用户或刚登出，可以跳过检查。
        # 主要检查点：当前请求的标识符是否与会话中存储的标识符匹配。
        if sess and ident != sess.get("_id", None):
            # **Basic 模式**: 只要会话不是永久性的，就标记为不新鲜（not fresh）。
            if mode == "basic" or sess.permanent:
                # 将会话标记为不新鲜（not fresh）
                if sess.get("_fresh") is not False:
                    sess["_fresh"] = False
                # 发送会话受保护的信号
                session_protected.send(app)
                # 返回 False，表示用户仍然可以访问，但状态已降级。
                return False
            # **Strong 模式**: 更严格，直接清除会话中的关键数据，并要求重新登录。
            elif mode == "strong":
                # 清除会话中的所有关键用户信息
                for k in SESSION_KEYS:
                    sess.pop(k, None)
                # 设置 _remember 为 'clear'，指示需要清除“记住我”Cookie
                sess["_remember"] = "clear"
                # 发送会话受保护的信号
                session_protected.send(app)
                # 返回 True，表示会话保护失败，需要重新认证。
                return True

        # 默认情况：会话保护未失败。
        return False

    def _load_user_from_remember_cookie(self, cookie):
        """尝试从“记住我”Cookie 中解码并加载用户。"""
        # 尝试解码 Cookie 值以获取用户 ID
        user_id = decode_cookie(cookie)
        # 如果成功解码出用户 ID
        if user_id is not None:
            # 将用户 ID 存入会话
            session["_user_id"] = user_id
            # 标记会话为不新鲜（not fresh），因为用户是通过持久 Cookie 登录的。
            session["_fresh"] = False
            # 初始化用户对象
            user = None
            # 如果定义了 user_loader 回调，则调用它加载用户对象。
            if self._user_callback:
                user = self._user_callback(user_id)
            # 如果成功加载到用户对象
            if user is not None:
                # 发送用户从 Cookie 加载的信号
                app = current_app._get_current_object()
                user_loaded_from_cookie.send(app, user=user)
                # 返回加载的用户对象
                return user
        # 如果解码失败或用户不存在，则返回 None。
        return None

    def _load_user_from_request(self, request):
        """尝试通过 request_loader 回调从当前请求中加载用户。"""
        # 如果定义了 request_loader 回调
        if self._request_callback:
            # 调用回调函数，传入请求对象，尝试加载用户。
            user = self._request_callback(request)
            # 如果成功加载到用户对象
            if user is not None:
                # 发送用户从请求加载的信号
                app = current_app._get_current_object()
                user_loaded_from_request.send(app, user=user)
                # 返回加载的用户对象
                return user
        # 如果回调未定义或未返回用户，则返回 None。
        return None

    def _update_remember_cookie(self, response):
        """在响应发送给客户端之前，更新“记住我”Cookie（如果需要）。"""
        # 获取应用配置，检查是否配置了每次请求都刷新 Cookie
        refresh_config = current_app.config.get("REMEMBER_COOKIE_REFRESH_EACH_REQUEST")
        # 如果会话中没有 _remember 标记，但配置了刷新，就设置一个 'set' 标记。
        # 这会触发 Cookie 过期时间的刷新。
        if "_remember" not in session and refresh_config:
            session["_remember"] = "set"

        # 检查会话中是否有需要处理的 _remember 操作（'set' 或 'clear'）
        if "_remember" in session:
            # 从会话中取出操作指令并移除标记
            operation = session.pop("_remember", None)

            # 如果操作是 'set' 且会话中存在用户 ID，则设置（或刷新）Cookie。
            if operation == "set" and "_user_id" in session:
                self._set_cookie(response)
            # 如果操作是 'clear'，则清除 Cookie。
            elif operation == "clear":
                self._clear_cookie(response)

        # 返回（可能已修改的）响应对象。
        return response

    def _set_cookie(self, response):
        """将“记住我”Cookie 设置到响应对象中。"""
        # 获取应用配置
        config = current_app.config
        # 获取 Cookie 名称，使用配置值或默认值
        cookie_name = config.get("REMEMBER_COOKIE_NAME", COOKIE_NAME)
        # 获取 Cookie 域名、路径
        domain = config.get("REMEMBER_COOKIE_DOMAIN")
        path = config.get("REMEMBER_COOKIE_PATH", "/")

        # 获取 Cookie 安全属性：安全（HTTPS）、仅限 HTTP、SameSite 策略
        secure = config.get("REMEMBER_COOKIE_SECURE", COOKIE_SECURE)
        httponly = config.get("REMEMBER_COOKIE_HTTPONLY", COOKIE_HTTPONLY)
        samesite = config.get("REMEMBER_COOKIE_SAMESITE", COOKIE_SAMESITE)

        # 确定 Cookie 的有效期（过期时间）
        # 优先使用会话中存储的 _remember_seconds
        if "_remember_seconds" in session:
            duration = timedelta(seconds=session["_remember_seconds"])
        else:
            # 否则使用应用配置或默认值
            duration = config.get("REMEMBER_COOKIE_DURATION", COOKIE_DURATION)

        # 准备要存储在 Cookie 中的数据：对用户 ID 进行编码
        data = encode_cookie(str(session["_user_id"]))

        # 如果 duration 是整数，转换为 timedelta 对象
        if isinstance(duration, int):
            duration = timedelta(seconds=duration)

        # 计算 Cookie 的过期时间（当前时间 + 有效期）
        try:
            expires = datetime.now(timezone.utc) + duration
        except TypeError as e:
            # 如果 duration 类型错误，抛出异常
            raise Exception(
                "REMEMBER_COOKIE_DURATION 必须是一个 datetime.timedelta 对象，"
                f"但实际得到的是: {duration}"
            ) from e

        # 使用 Flask 的 response.set_cookie 方法实际设置 Cookie
        response.set_cookie(
            cookie_name,
            value=data,          # Cookie 值（编码后的用户 ID）
            expires=expires,     # 过期时间
            domain=domain,       # 作用域域名
            path=path,           # 作用域路径
            secure=secure,       # 仅通过 HTTPS 传输
            httponly=httponly,   # 仅限 HTTP(S)，JavaScript 无法访问
            samesite=samesite,   # SameSite 策略，防止 CSRF
        )

    def _clear_cookie(self, response):
        """从响应对象中清除“记住我”Cookie。"""
        # 获取应用配置
        config = current_app.config
        # 获取 Cookie 名称、域名、路径
        cookie_name = config.get("REMEMBER_COOKIE_NAME", COOKIE_NAME)
        domain = config.get("REMEMBER_COOKIE_DOMAIN")
        path = config.get("REMEMBER_COOKIE_PATH", "/")
        # 使用 Flask 的 response.delete_cookie 方法清除 Cookie
        response.delete_cookie(cookie_name, domain=domain, path=path)