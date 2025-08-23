from datetime import timedelta

#: The default name of the "remember me" cookie (``remember_token``)
# "remember me" cookie 的默认名称 (``remember_token``)
COOKIE_NAME = "remember_token"

#: The default time before the "remember me" cookie expires (365 days).
# "remember me" cookie 过期之前的默认时间 (365 天)。
COOKIE_DURATION = timedelta(days=365)

#: Whether the "remember me" cookie requires Secure; defaults to ``False``
# "remember me" cookie 是否需要 Secure 属性；默认为 ``False``。
COOKIE_SECURE = False

#: Whether the "remember me" cookie uses HttpOnly or not; defaults to ``True``
# "remember me" cookie 是否使用 HttpOnly；默认为 ``True``。
COOKIE_HTTPONLY = True

#: Whether the "remember me" cookie requires same origin; defaults to ``None``
# "remember me" cookie 是否需要同源；默认为 ``None``。
COOKIE_SAMESITE = None

#: The default flash message to display when users need to log in.
# 当用户需要登录时显示的默认闪现消息。
LOGIN_MESSAGE = "Please log in to access this page."

#: The default flash message category to display when users need to log in.
# 当用户需要登录时显示的默认闪现消息类别。
LOGIN_MESSAGE_CATEGORY = "message"

#: The default flash message to display when users need to reauthenticate.
# 当用户需要重新认证时显示的默认闪现消息。
REFRESH_MESSAGE = "Please reauthenticate to access this page."

#: The default flash message category to display when users need to
#: reauthenticate.
# 当用户需要重新认证时显示的默认闪现消息类别。
REFRESH_MESSAGE_CATEGORY = "message"

#: The default attribute to retrieve the str id of the user
# 用于获取用户 str id 的默认属性。
ID_ATTRIBUTE = "get_id"

#: A set of session keys that are populated by Flask-Login. Use this set to
#: purge keys safely and accurately.
# 由 Flask-Login 填充的一组 session 键。使用此集合可以安全、准确地清除键。
SESSION_KEYS = {
    "_user_id",
    "_remember",
    "_remember_seconds",
    "_id",
    "_fresh",
    "next",
}

#: A set of HTTP methods which are exempt from `login_required` and
#: `fresh_login_required`. By default, this is just ``OPTIONS``.
# 一组不受 `login_required` 和 `fresh_login_required` 限制的 HTTP 方法。默认情况下，只有 ``OPTIONS``。
EXEMPT_METHODS = {"OPTIONS"}
    # {"OPTIONS"}: 这是一个只包含一个元素 "OPTIONS" 的集合。
        # "OPTIONS": 这是一个 HTTP 方法。根据 HTTP/1.1 规范 (RFC 7231)，OPTIONS 请求用于获取目标资源所支持的通信选项。客户端（如浏览器）在发送一些“复杂”的请求（例如包含自定义头或使用 PUT/DELETE 方法的请求）之前，会先发送一个 OPTIONS 请求进行“预检”（preflight request），以确定服务器是否允许该实际请求。
    # 为什么 OPTIONS 被豁免？
        # 如果 OPTIONS 请求也受到登录保护，那么在跨域（CORS）场景下会出现问题：
            # 浏览器在发送一个需要身份验证的 POST 请求前，会先发送一个 OPTIONS 预检请求。
            # 如果这个 OPTIONS 请求返回 401（未授权），浏览器会认为整个请求序列不被允许，从而阻止后续真正的 POST 请求发送。
            # 即使用户已经登录，这个流程也会被阻断，导致功能无法正常使用。
            # 因此，将 OPTIONS 方法豁免于登录检查是必要的实践，以确保 CORS 预检请求能够成功通过，从而让后续的实际请求（如 POST, PUT, DELETE）得以正常进行。服务器的安全性仍然由后续的实际请求的认证机制来保证。

#: If true, the page the user is attempting to access is stored in the session
#: rather than a url parameter when redirecting to the login view; defaults to
#: ``False``.
# 如果为 True，当重定向到登录视图时，用户试图访问的页面会存储在 session 中，而不是作为 URL 参数；默认为 ``False``。
USE_SESSION_FOR_NEXT = False