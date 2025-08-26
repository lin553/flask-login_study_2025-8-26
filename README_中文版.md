"""
Flask-Login 提供了为 [Flask][] 框架的用户会话管理功能。
它处理了登录、登出以及在较长时间内记住用户会话等常见任务。

Flask-Login 不与任何特定的数据库系统或权限模型绑定。
唯一的前提是，你的用户对象需要实现几个方法，
并且你需要提供一个回调函数给这个扩展，该函数能够根据用户的 ID 加载用户。

在 <https://flask-login.readthedocs.io> 阅读完整的文档。

[Flask]: https://flask.palletsprojects.com
"""

# 导入必要的模块
import flask
import flask_login

# 创建一个 Flask 应用实例
app = flask.Flask(__name__)
# 设置应用的密钥，用于会话加密等。在生产环境中，这必须是一个真正随机的、保密的强密钥！
app.secret_key = "super secret string"  # 改变这个值！

# 创建一个 LoginManager 实例
login_manager = flask_login.LoginManager()
# 将 LoginManager 初始化并绑定到 Flask 应用 app 上
login_manager.init_app(app)


# 为了保持简单，我们将使用一个基本的 `User` 类和一个字典来代表一个用户数据库。
# 在真实的应用程序中，这将是一个实际的持久化层（如 SQL 数据库、NoSQL 数据库等）。
# 然而，重要的是要指出，这正是 Flask-Login 的一个特性：
# 它不关心你的数据是如何存储的，只要你告诉它如何检索数据即可！
class User(flask_login.UserMixin):
    def __init__(self, email, password):
        # 在这个简单示例中，使用 email 作为用户的唯一标识符 (ID)
        self.id = email
        self.password = password

# 模拟一个用户数据库，这里是一个字典，键是用户名（email），值是 User 对象
users = {"leafstorm": User("leafstorm", "secret")}


# 我们还需要告诉登录管理器如何从一个用户 ID 加载用户，
# 这通过定义其 `user_loader` 回调函数来实现。
# 如果找不到用户，该函数应返回 `None`。
@login_manager.user_loader
def user_loader(id):
    # 根据用户 ID (这里是 email) 从 "数据库" (users 字典) 中获取用户对象
    # 如果 ID 不存在，dict.get() 会返回 None，符合要求
    return users.get(id)


# 现在我们准备好了，可以定义视图函数了。
# 登录视图会用认证信息填充会话。
# 受保护的视图仅对已认证的用户可用；否则访问它会显示错误。
# 登出视图会清除会话。

# GET 请求：显示登录表单
@app.get("/login")
def login():
    # 返回一个简单的 HTML 表单，用于输入邮箱和密码
    return """<form method=post>
      Email: <input name="email"><br>
      Password: <input name="password" type=password><br>
      <button>Log In</button>
    </form>"""


# POST 请求：处理登录表单提交
@app.post("/login")
def login():
    # 从表单数据中获取 email，并尝试从 "数据库" 中查找对应的用户
    user = users.get(flask.request.form["email"])

    # 检查：用户是否存在 且 密码是否正确
    # 注意：真实应用中密码必须哈希存储，这里仅作演示！
    if user is None or user.password != flask.request.form["password"]:
        # 如果用户不存在或密码错误，重定向回登录页面
        return flask.redirect(flask.url_for("login"))

    # 使用 Flask-Login 的 login_user 函数登录用户
    # 这会将用户信息存储在会话中，标记用户为已登录状态
    flask_login.login_user(user)
    # 登录成功，重定向到受保护的页面
    return flask.redirect(flask.url_for("protected"))


# 受保护的路由
@app.route("/protected")
@flask_login.login_required # 装饰器：确保只有已登录用户才能访问此视图
def protected():
    # 使用 render_template_string 渲染一个简单的字符串模板
    # flask_login.current_user 是一个 LocalProxy，它在运行时指向当前登录的用户对象
    return flask.render_template_string(
        "Logged in as: {{ user.id }}", # 模板内容
        user=flask_login.current_user # 传递给模板的上下文变量
    )


# 登出路由
@app.route("/logout")
def logout():
    # 使用 Flask-Login 的 logout_user 函数登出用户
    # 这会清除会话中的用户信息，标记用户为已登出状态
    flask_login.logout_user()
    return "Logged out"


# 如果你想直接运行这个脚本，可以加上这行
# if __name__ == "__main__":
#     app.run(debug=True)