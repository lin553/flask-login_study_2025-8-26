'''

装饰器的常见用途
日志记录 (Logging)：在函数执行前后记录信息。
性能测试 (Timing)：测量函数执行时间。
权限检查 (Authorization)：检查用户是否有权限执行某个操作（如 Flask-Login 的 @login_required）。
输入验证 (Validation)：检查函数参数是否有效。
缓存 (Caching)：缓存函数的返回值，避免重复计算。
事务管理 (Transactions)：在数据库操作前后开启/提交事务。
异常处理 (Error Handling)：统一处理函数中的异常。
在 Flask-Login 中的应用
你之前看到的 @login_required 和 @login_manager.user_loader 都是装饰器：

@login_required：这是一个函数装饰器。它检查用户是否登录。如果未登录，则重定向到登录页；如果已登录，则允许原视图函数执行。
                它“装饰”在路由函数上，为其添加了身份验证功能。
@login_manager.user_loader：这是一个回调注册装饰器。它本身是一个方法（user_loader），被设计成可以用 @ 语法调用。
                            它的作用是将被它“装饰”的函数（load_user）注册为从会话加载用户的回调函数。
总结
装饰器是 Python 中一个强大的功能，用于在不修改原函数代码的情况下，增强或修改其行为。
语法是 @decorator_name。
本质上是“函数接收函数作为参数，并返回一个新函数”。
广泛应用于日志、计时、权限、缓存等场景。
记得使用 @wraps 来保留被装饰函数的元数据。

'''