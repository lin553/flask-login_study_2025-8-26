===========
Flask-Login
===========
.. currentmodule:: flask_login

Flask-Login provides user session management for Flask. It handles the common
tasks of logging in, logging out, and remembering your users' sessions over
extended periods of time.

它将：

- 在 `Flask Session`_ 中存储活跃用户的 ID，并让你能轻松地登录和登出他们。
- 让你限制视图只能由已登录（或已登出）的用户访问。(`login_required`)
- 处理通常比较棘手的“记住我”（remember me）功能。
- 帮助保护用户的会话不被窃取 Cookie 的小偷盗取。

然而，它**不会**：

- 对你强加特定的数据库或其他存储方式。你完全掌控用户是如何被加载的。
- 限制你只能使用用户名/密码、OpenID 或任何其他认证方法。
- 处理超出“已登录或未登录”范围的权限。
- 处理用户注册或账户找回。

安装
============
使用 pip 安装扩展::

    $ pip install flask-login


配置你的应用
============================
使用 Flask-Login 的应用中最重要的部分是 `LoginManager` 类。你应该在代码的某个地方为你的应用创建一个，像这样::

    from flask_login import LoginManager
    login_manager = LoginManager()

登录管理器包含了让你的应用和 Flask-Login 协同工作的代码，例如如何从 ID 加载用户、当用户需要登录时将他们重定向到哪里等等。

一旦实际的应用对象被创建，你可以使用以下方式为其配置登录功能::

    login_manager.init_app(app)

默认情况下，Flask-Login 使用会话（sessions）进行认证。这意味着你必须在你的应用上设置一个密钥（secret key），否则 Flask 会给你一个错误信息，告诉你需要这样做。参见 `Flask 文档关于会话的部分`_ 来了解如何设置密钥。

*警告*：**务必**使用“如何生成好的密钥”部分中给出的命令来生成你自己的密钥。**不要**使用示例中的密钥。

要完全理解可用的配置项，请参考 `源代码`_。

它是如何工作的
============
你需要提供一个 `~LoginManager.user_loader` 回调函数。这个回调函数用于从会话中存储的用户 ID 重新加载用户对象。它应该接收一个用户的 `str` 类型 ID，并返回相应的用户对象。例如::

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

如果 ID 无效，它应该返回 `None`（**而不是抛出异常**）。在这种情况下，该 ID 将被手动从会话中移除，处理将继续进行。

你的用户类
===============
你用来表示用户的类需要实现以下属性和方法：

`is_authenticated`
    这个属性应该在用户已认证时返回 `True`，即他们提供了有效的凭据。（只有已认证的用户才能满足 `login_required` 的条件。）

`is_active`
    这个属性应该在用户是活跃状态时返回 `True` —— 除了已认证，他们的账户也已激活、未被暂停，或者你的应用设定的任何拒绝账户的条件。非活跃账户可能无法登录（当然，强制登录除外）。

`is_anonymous`
    这个属性应该在用户是匿名用户时返回 `True`。（真实用户应该返回 `False`。）

`get_id()`
    这个方法必须返回一个能唯一标识该用户的 `str` 字符串，并且可以用于从 `~LoginManager.user_loader` 回调中加载用户。请注意，这**必须**是一个 `str` 类型 —— 如果 ID 本质上是 `int` 或其他类型，你需要将其转换为 `str`。

为了更容易地实现用户类，你可以继承 `UserMixin`，它为所有这些属性和方法提供了默认实现。（但这不是必须的。）

登录示例
=============

一旦用户通过了身份验证，你可以使用 `login_user` 函数让他们登录。

    例如：

.. code-block:: python

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # 这里我们使用某种类来表示和验证我们的
        # 客户端表单数据。例如，WTForms 是一个库，它将
        # 为我们处理这个，我们使用一个自定义的 LoginForm 来验证。
        form = LoginForm()
        if form.validate_on_submit():
            # 登录并验证用户。
            # user 应该是你的 `User` 类的一个实例
            login_user(user)

            flask.flash('登录成功。')

            next = flask.request.args.get('next')
            # url_has_allowed_host_and_scheme 应该检查 url 是否安全
            # 用于重定向，即它是否匹配请求的主机。
            # 参见 Django 的 url_has_allowed_host_and_scheme 作为例子。
            if not url_has_allowed_host_and_scheme(next, request.host):
                return flask.abort(400)

            return flask.redirect(next or flask.url_for('index'))
        return flask.render_template('login.html', form=form)

*警告*：你**必须**验证 `next` 参数的值。如果你不这样做，你的应用将容易受到开放重定向漏洞的攻击。关于 `url_has_allowed_host_and_scheme` 的实现示例，请参见 Django 的 `实现 <https://github.com/django/django/blob/4.0/django/utils/http.py#L239>`_。

就是这么简单。然后你就可以使用 `current_user` 代理来访问已登录的用户，这个代理在每个模板中都可用::

    {% if current_user.is_authenticated %}
      你好 {{ current_user.name }}!
    {% endif %}

需要用户登录才能访问的视图可以使用 `login_required` 装饰器进行装饰::

    @app.route("/settings")
    @login_required
    def settings():
        pass

当用户准备登出时::

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(somewhere)

他们将被登出，其会话的任何 Cookie 都将被清理。

自定义登录流程
=============================
默认情况下，当用户尝试访问一个需要登录的视图但未登录时，Flask-Login 会闪现一条消息并重定向他们到登录视图。（如果未设置登录视图，它将返回 401 错误。）

登录视图的名称可以通过 `LoginManager.login_view` 设置。例如::

    login_manager.login_view = "users.login"

默认闪现的消息是 ``请登录以访问此页面。`` 要自定义消息，请设置 `LoginManager.login_message`::

    login_manager.login_message = u"请登录以使用此页面。"  # 示例：世界语消息

要自定义消息类别，请设置 `LoginManager.login_message_category`::

    login_manager.login_message_category = "info"

当重定向到登录视图时，查询字符串中会有一个 ``next`` 变量，它表示用户试图访问的页面。或者，如果 `USE_SESSION_FOR_NEXT` 为 `True`，该页面会存储在会话中，键为 ``next``。

如果你想进一步自定义该流程，可以用 `LoginManager.unauthorized_handler` 装饰一个函数::

    @login_manager.unauthorized_handler
    def unauthorized():
        # 做一些事情
        return a_response

例如：你正在将 Flask-Login 与 Flask-RESTful 一起使用。在你的 API（名为 api 的蓝图）中，你不想重定向到登录页面，而是想返回“未授权”状态码。::

    from flask import redirect, url_for, request
    from http import HTTPStatus
    @login_manager.unauthorized_handler
    def unauthorized():
        if request.blueprint == 'api':
            abort(HTTPStatus.UNAUTHORIZED)
        return redirect(url_for('site.login'))


使用请求加载器进行自定义登录
=================================
有时你希望在不使用 Cookie 的情况下登录用户，例如使用请求头（header）的值或作为查询参数传递的 API 密钥。在这种情况下，你应该使用 `~LoginManager.request_loader` 回调函数。这个回调函数的行为应该与你的 `~LoginManager.user_loader` 回调相同，只是它接收的是 Flask 请求对象，而不是用户 ID。

例如，支持从 URL 参数和使用 `Authorization` 头的 Basic Auth 两种方式登录::

    @login_manager.request_loader
    def load_user_from_request(request):

        # 首先，尝试使用 url 参数中的 api_key 登录
        api_key = request.args.get('api_key')
        if api_key:
            user = User.query.filter_by(api_key=api_key).first()
            if user:
                return user

        # 接着，尝试使用 Basic Auth 登录
        api_key = request.headers.get('Authorization')
        if api_key:
            api_key = api_key.replace('Basic ', '', 1) # 移除 "Basic " 前缀
            try:
                api_key = base64.b64decode(api_key) # Base64 解码
            except TypeError:
                pass # 解码失败则忽略
            user = User.query.filter_by(api_key=api_key).first()
            if user:
                return user

        # 最后，如果两种方法都未能登录用户，则返回 None
        return None

注释：这个例子展示了如何从不同来源（URL 参数、HTTP 头）提取凭证（API Key），并用它来查找用户。这非常适合无状态的 API 认证。

匿名用户
===============
默认情况下，当用户实际上未登录时，`current_user` 会被设置为一个 `AnonymousUserMixin` 对象。它具有以下属性和方法：

- `is_active` 为 `False`
- `is_authenticated` 为 `False`
- `is_anonymous` 为 `True`
- `get_id()` 返回 `None`

如果你对匿名用户有自定义需求（例如，他们需要有一个权限字段），你可以向 `LoginManager` 提供一个可调用对象（可以是一个类或工厂函数），用于创建匿名用户::

    login_manager.anonymous_user = MyAnonymousUser

注释：`MyAnonymousUser` 应该是一个类或返回匿名用户实例的函数。这允许你为未登录用户提供更丰富的默认行为或权限。

记住我
===========
默认情况下，当用户关闭浏览器时，Flask 会话（Session）会被删除，用户也会被登出。“记住我”功能可以防止用户在关闭浏览器时意外地被登出。这**不**意味着在用户登出后，会记住或预先填写登录表单中的用户名或密码。

“记住我”功能实现起来可能比较棘手。然而，Flask-Login 使其几乎变得透明——只需在调用 `login_user` 时传入 ``remember=True``。一个 Cookie 会被保存在用户的计算机上，然后如果用户的 ID 不在会话中，Flask-Login 会自动从该 Cookie 中恢复用户 ID。Cookie 的过期时间可以通过 `REMEMBER_COOKIE_DURATION` 配置项设置，也可以直接传给 `login_user`。该 Cookie 是防篡改的，因此如果用户篡改了它（例如，将自己的用户 ID 替换为别人的），该 Cookie 将仅仅被拒绝，就像它不存在一样。

这种级别的功能是自动处理的。然而，你可以（并且应该，如果你的应用处理任何敏感数据的话）提供额外的基础设施来增强你的“记住我” Cookie 的安全性。

替代令牌
==================
使用用户 ID 作为“记住我”令牌的值意味着你必须更改用户的 ID 才能使其登录会话失效。改进这一点的一种方法是使用一个替代的用户 ID 而不是用户的主 ID。例如::

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(alternative_id=user_id).first()

然后，你用户类的 `~UserMixin.get_id` 方法应返回替代 ID，而不是用户的主 ID::

    def get_id(self):
        return str(self.alternative_id)

这样，当你更改用户的密码时，就可以自由地将用户的替代 ID 更改为一个新的随机生成的值，这将确保他们旧的认证会话将不再有效。请注意，替代 ID 仍然必须唯一地标识用户……把它看作是用户的第二个用户 ID。

注释：这是一个重要的安全最佳实践。直接使用主键（如数据库自增ID）作为 remember token 的话，一旦用户修改密码，旧的 remember token 依然有效。使用一个可变的、独立的 `alternative_id`（或称为 `session_token`）可以实现“使所有其他设备登出”或“密码更改后旧会话失效”的功能。

新鲜登录
============
当用户登录时，他们的会话被标记为“新鲜的”（fresh），这表示他们实际上在该会话中进行了身份验证。当他们的会话被销毁并使用“记住我” Cookie 重新登录时，它被标记为“非新鲜的”（non-fresh）。`login_required` 不区分会话的新鲜度，这对大多数页面来说是没问题的。然而，像更改个人信息这样的敏感操作应该要求一个新鲜的登录。（像更改密码这样的操作，无论何时都应该要求重新输入密码。）

`fresh_login_required` 除了验证用户是否已登录外，还会确保他们的登录是新鲜的。如果不是，它会将他们重定向到一个页面，在那里他们可以重新输入凭据。你可以通过设置 `LoginManager.refresh_view`、`~LoginManager.needs_refresh_message` 和 `~LoginManager.needs_refresh_message_category` 来以与自定义 `login_required` 相同的方式来定制其行为::

    login_manager.refresh_view = "accounts.reauthenticate"
    login_manager.needs_refresh_message = (
        u"为了保护您的账户，请重新认证以访问此页面。"
    )
    login_manager.needs_refresh_message_category = "info"

或者，通过提供自己的回调函数来处理刷新::

    @login_manager.needs_refresh_handler
    def refresh():
        # 做一些事情
        return a_response

要再次将一个会话标记为新鲜的，请调用 `confirm_login` 函数。

注释：`fresh_login_required` 是保护敏感操作的关键。例如，访问 `/profile/edit` 可能只需要 `login_required`，但访问 `/profile/change-password` 或 `/profile/delete` 则应使用 `fresh_login_required`，以确保是用户本人在操作。

Cookie 设置
===============
Cookie 的详细信息可以在应用设置中进行自定义。

====================================== =================================================
`REMEMBER_COOKIE_NAME`                 用于存储“记住我”信息的 Cookie 的名称。
                                       **默认值：** ``remember_token``
`REMEMBER_COOKIE_DURATION`             Cookie 过期前的时间长度，可以是 `datetime.timedelta` 对象或整数秒。
                                       **默认值：** 365天（1个非闰格里高利年）
`REMEMBER_COOKIE_DOMAIN`               如果“记住我”Cookie 应该跨域使用，请在此处设置域名（例如 ``.example.com`` 将允许 Cookie 在 ``example.com`` 的所有子域上使用）。
                                       **默认值：** `None`
`REMEMBER_COOKIE_PATH`                 将“记住我”Cookie 限制在特定路径下。
                                       **默认值：** ``/``
`REMEMBER_COOKIE_SECURE`               将“记住我”Cookie 的范围限制在安全通道（通常是 HTTPS）内。
                                       **默认值：** `False`
`REMEMBER_COOKIE_HTTPONLY`             防止“记住我”Cookie 被客户端脚本访问。
                                       **默认值：** `True`
`REMEMBER_COOKIE_REFRESH_EACH_REQUEST` 如果设置为 `True`，则每次请求时都会刷新 Cookie，从而延长其生命周期。其工作方式类似于 Flask 的 `SESSION_REFRESH_EACH_REQUEST`。
                                       **默认值：** `False`
`REMEMBER_COOKIE_SAMESITE`             将“记住我”Cookie 限制在第一方或同站上下文中。
                                       **默认值：** `None`
====================================== =================================================

注释：这些配置项对于安全和功能至关重要。
- `REMEMBER_COOKIE_SECURE=True` **强烈建议在生产环境中使用 HTTPS 时设置**，以防止 Cookie 在非加密连接中被窃取。
- `REMEMBER_COOKIE_HTTPONLY=True` 是默认且推荐的，防止 XSS 攻击窃取 Cookie。
- `REMEMBER_COOKIE_SAMESITE` 可以设置为 `"Lax"` 或 `"Strict"` 来帮助防范 CSRF 攻击。
- `REMEMBER_COOKIE_REFRESH_EACH_REQUEST` 需要权衡：它能提供更好的用户体验（会话不断延长），但也增加了安全风险（会话长期有效）。



会话保护
==================
虽然上述功能有助于保护你的“记住我”令牌免受 Cookie 窃贼的侵害，但会话 Cookie 仍然存在漏洞。Flask-Login 包含了会话保护功能，以帮助防止用户的会话被窃取。

你可以在 `LoginManager` 上或应用的配置中配置会话保护。如果启用，它可以运行在 `basic`（基本）或 `strong`（强）模式下。要在 `LoginManager` 上设置，将 `~LoginManager.session_protection` 属性设置为 ``"basic"`` 或 ``"strong"``::

    login_manager.session_protection = "strong"

或者，要禁用它::

    login_manager.session_protection = None

默认情况下，它以 ``"basic"`` 模式激活。可以通过将应用配置中的 `SESSION_PROTECTION` 设置为 `None`、``"basic"`` 或 ``"strong"`` 来禁用。

当会话保护处于活动状态时，每次请求，它都会为用户的计算机生成一个标识符（基本上是 IP 地址和用户代理的加密哈希值）。如果会话没有关联的标识符，则会将生成的标识符存储起来。如果它已有标识符，并且与生成的标识符匹配，则请求是正常的。

如果在 `basic` 模式下标识符不匹配，或者会话是永久性的（permanent），那么会话将仅被标记为非新鲜（non-fresh），任何需要新鲜登录的操作都将强制用户重新进行身份验证。（当然，你必须已经在适当的地方使用了新鲜登录，这个功能才能生效。）

如果在 `strong` 模式下，对于非永久性会话，标识符不匹配，那么整个会话（以及存在的“记住我”令牌）将被删除。

注释：这是一个重要的安全特性。
- **`basic` 模式**：更宽容，仅将会话降级为非新鲜，要求敏感操作重新认证。适用于大多数场景。
- **`strong` 模式**：更严格，直接销毁会话和记住令牌，强制用户完全重新登录。适用于处理极高敏感数据的应用。
- 保护原理是检测用户设备（IP+User-Agent）的显著变化。注意，这可能导致在用户使用代理、切换网络（如WiFi到移动数据）或更新浏览器时出现误判。

为 API 禁用会话 Cookie
=================================
在向 API 进行身份验证时，你可能希望禁用设置 Flask 会话 Cookie。为此，可以使用一个自定义的会话接口（session interface），该接口根据你在请求上设置的标志来决定是否保存会话。例如::

    from flask import g
    from flask.sessions import SecureCookieSessionInterface
    from flask_login import user_loaded_from_request

    @user_loaded_from_request.connect
    def user_loaded_from_request(app, user=None):
        g.login_via_request = True # 在请求上下文中设置一个标志


    class CustomSessionInterface(SecureCookieSessionInterface):
        """防止从 API 请求创建会话。"""
        def save_session(self, *args, **kwargs):
            if g.get('login_via_request'): # 如果是通过 request_loader 登录的
                return # 不保存会话 Cookie
            return super(CustomSessionInterface, self).save_session(*args, **kwargs)

    app.session_interface = CustomSessionInterface()

这可以防止在用户使用你的 `~LoginManager.request_loader` 进行身份验证时设置 Flask 会话 Cookie。

注释：这是构建无状态 API 的关键技巧。当 API 使用 API Key 或 Bearer Token 认证时，不应创建有状态的 Flask Session Cookie，以避免不必要的服务器状态和潜在的会话固定攻击。此代码利用 `user_loaded_from_request` 信号来标记通过 `request_loader` 登录的请求。

自动化测试
=================
为了让你更容易编写自动化测试，Flask-Login 提供了一个简单的、自定义的测试客户端类，它可以为你设置用户的登录 Cookie：`~FlaskLoginClient`。要使用这个自定义测试客户端类，请将其分配给你的应用对象的 `test_client_class` 属性，如下所示::

    from flask_login import FlaskLoginClient

    app.test_client_class = FlaskLoginClient

接下来，像往常一样使用 `app.test_client()` 方法创建一个测试客户端。然而，现在你可以向此方法传递一个用户对象，你的客户端将自动以该用户身份登录！

.. code-block:: python

    def test_request_with_logged_in_user():
        user = User.query.get(1)
        with app.test_client(user=user) as client:
            # 此请求已自动以用户 1 的身份登录！
            client.get("/")

你也可以传递 ``fresh_login``（``bool`` 类型，默认为 ``True``）来标记当前登录是新鲜的还是非新鲜的。

请注意，你必须使用关键字参数，而不是位置参数。例如，``test_client(user=user)`` 可以工作，但 ``test_client(user)`` 将无法工作。

由于此自定义测试客户端类的实现方式，你可能需要**禁用会话保护**才能使你的测试正常工作。如果启用了会话保护，在使用测试客户端执行请求时，登录会话将在 `basic` 模式下被标记为非新鲜，或在 `strong` 模式下被直接拒绝。

注释：`FlaskLoginClient` 极大地简化了需要认证的测试。但需注意：
1.  **会话保护冲突**：测试客户端模拟的请求通常不会产生与真实浏览器相同的 IP/UA，因此会触发会话保护。在测试配置中设置 `SESSION_PROTECTION = None` 是常见做法。
2.  **参数传递**：必须使用 `user=...` 和 `fresh_login=...` 这样的关键字参数。

本地化
============
默认情况下，`LoginManager` 使用 ``flash`` 在用户需要登录时显示消息。这些消息是英文的。如果你需要本地化，请将 `LoginManager` 的 `localize_callback` 属性设置为一个函数，该函数会在消息发送到 ``flash`` 之前被调用，例如 ``gettext``。此函数将接收消息作为参数，其返回值将代替原消息被发送到 ``flash``。

注释：这是实现多语言应用的重要步骤。你可以将其设置为 `gettext.gettext` 或 `babel.gettext` 等函数，以便将 "Please log in to access this page." 等提示翻译成中文或其他语言。

API 文档
=================
此文档是从 Flask-Login 的源代码自动生成的。


配置登录
-----------------

.. module:: flask_login

.. autoclass:: LoginManager

   .. automethod:: init_app

   .. automethod:: unauthorized

   .. automethod:: needs_refresh

   .. rubric:: 通用配置

   .. automethod:: user_loader

   .. automethod:: request_loader

   .. attribute:: anonymous_user

      一个类或工厂函数，用于生成匿名用户，当无人登录时使用。

   .. rubric:: `unauthorized` 配置

   .. attribute:: login_view

      当用户需要登录时，重定向到的视图名称。（如果认证机制在应用外部，也可以是绝对 URL。）

   .. attribute:: blueprint_login_views

      这与 login_view 类似，但在使用蓝图时使用。它是一个字典，可以为不同的蓝图存储多个重定向视图。格式为蓝图名称作为键，重定向路由作为值。

   .. attribute:: login_message

      当用户被重定向到登录页面时要闪现（flash）的消息。

   .. automethod:: unauthorized_handler

   .. rubric:: `needs_refresh` 配置

   .. attribute:: refresh_view

      当用户需要重新认证时，重定向到的视图名称。

   .. attribute:: needs_refresh_message

      当用户被重定向到重新认证页面时要闪现（flash）的消息。

   .. automethod:: needs_refresh_handler


登录机制
----------------
.. data:: current_user

   当前用户的代理对象。

.. autofunction:: login_fresh

.. autofunction:: login_remembered

.. autofunction:: login_user

.. autofunction:: logout_user

.. autofunction:: confirm_login


保护视图
----------------
.. autofunction:: login_required

.. autofunction:: fresh_login_required


用户对象助手
-------------------
.. autoclass:: UserMixin
   :members:

.. autoclass:: AnonymousUserMixin
   :members:


工具
---------
.. autofunction:: login_url

.. autoclass:: FlaskLoginClient


信号
-------
请参阅 `Flask 文档关于信号`_ 以了解如何在代码中使用这些信号。

.. data:: user_logged_in

   当用户登录时发送。除了应用（发送者）外，还会传递 `user` 参数，即正在登录的用户。

.. data:: user_logged_out

   当用户登出时发送。除了应用（发送者）外，还会传递 `user` 参数，即正在登出的用户。

.. data:: user_login_confirmed

   当用户登录被确认，标记为新鲜时发送。（正常登录不会调用此信号。）
   除了应用外，不接收其他参数。

.. data:: user_unauthorized

   当在 `LoginManager` 上调用 `unauthorized` 方法时发送。除了应用外，不接收其他参数。

.. data:: user_needs_refresh

   当在 `LoginManager` 上调用 `needs_refresh` 方法时发送。除了应用外，不接收其他参数。

.. data:: session_protected

   每当会话保护生效，会话被标记为非新鲜或被删除时发送。除了应用外，不接收其他参数。

.. _source code: https://github.com/maxcountryman/flask-login/tree/main/src/flask_login
.. _Flask documentation on signals: https://flask.palletsprojects.com/en/latest/signals/
.. _this Flask Snippet: https://web.archive.org/web/20120517003641/http://flask.pocoo.org/snippets/62/
.. _Flask Session: https://flask.palletsprojects.com/en/latest/api/#sessions
.. _Flask documentation on sessions: https://flask.palletsprojects.com/en/latest/quickstart/#sessions

