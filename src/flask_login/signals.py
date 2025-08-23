from flask.signals import Namespace

_signals = Namespace()

#: Sent when a user is logged in. In addition to the app (which is the
#: sender), it is passed `user`, which is the user being logged in.
# 当用户登录时发送。除了应用实例（作为发送者）外，还会传递 `user` 参数，即正在登录的用户。
user_logged_in = _signals.signal("logged-in")

#: Sent when a user is logged out. In addition to the app (which is the
#: sender), it is passed `user`, which is the user being logged out.
# 当用户登出时发送。除了应用实例（作为发送者）外，还会传递 `user` 参数，即正在登出的用户。
user_logged_out = _signals.signal("logged-out")

#: Sent when the user is loaded from the cookie. In addition to the app (which
#: is the sender), it is passed `user`, which is the user being reloaded.
# 当从 Cookie 中加载用户时发送。除了应用实例（作为发送者）外，还会传递 `user` 参数，即正在重新加载的用户。
user_loaded_from_cookie = _signals.signal("loaded-from-cookie")

#: Sent when the user is loaded from the request. In addition to the app (which
#: is the #: sender), it is passed `user`, which is the user being reloaded.
# 当从请求中加载用户时发送。除了应用实例（作为发送者）外，还会传递 `user` 参数，即正在重新加载的用户。
user_loaded_from_request = _signals.signal("loaded-from-request")

#: Sent when a user's login is confirmed, marking it as fresh. (It is not
#: called for a normal login.)
#: It receives no additional arguments besides the app.
# 当确认用户的登录状态，并将其标记为“新鲜”时发送。（普通登录不会调用此信号。）
# 除了应用实例外，不接收其他额外参数。
user_login_confirmed = _signals.signal("login-confirmed")

#: Sent when the `unauthorized` method is called on a `LoginManager`. It
#: receives no additional arguments besides the app.
# 当在 `LoginManager` 上调用 `unauthorized` 方法时发送。除了应用实例外，不接收其他额外参数。
user_unauthorized = _signals.signal("unauthorized")

#: Sent when the `needs_refresh` method is called on a `LoginManager`. It
#: receives no additional arguments besides the app.
# 当在 `LoginManager` 上调用 `needs_refresh` 方法时发送。除了应用实例外，不接收其他额外参数。
user_needs_refresh = _signals.signal("needs-refresh")

#: Sent whenever the user is accessed/loaded
#: receives no additional arguments besides the app.
# 每当用户被访问或加载时发送。除了应用实例外，不接收其他额外参数。
user_accessed = _signals.signal("accessed")

#: Sent whenever session protection takes effect, and a session is either
#: marked non-fresh or deleted. It receives no additional arguments besides
#: the app.
# 每当会话保护机制生效（会话被标记为非新鲜或被删除）时发送。除了应用实例外，不接收其他额外参数。
session_protected = _signals.signal("session-protected")