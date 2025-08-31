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



