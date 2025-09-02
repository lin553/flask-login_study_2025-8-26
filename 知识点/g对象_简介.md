在 Flask 框架中，`g` 是一个**全局对象 (global object)**，但它**不是**传统意义上的全局变量。它的作用是**在一个请求的生命周期内，存储和共享数据**。

### `g` 对象的核心特性

1.  **请求局部 (Request-Local)**：
    *   `g` 中存储的数据**只在当前这个 HTTP 请求的处理过程中有效**。
    *   不同的请求拥有各自独立的 `g` 对象实例，互不干扰。
    *   请求结束时，`g` 对象中的所有数据会自动被清理。

2.  **全局可访问 (Globally Accessible within a Request)**：
    *   在同一个请求的任何地方（视图函数、模板、before_request 处理器等），都可以通过 `from flask import g` 来导入并访问它。

3.  **用途**：
    *   存储数据库连接、API 客户端实例等需要在多个函数间共享的资源。
    *   在 `@app.before_request` 中设置数据，供后续的视图函数使用。

---

### `g` 对象的“成员”（属性）

`g` 对象本身没有预定义的固定成员。它就像一个**空的容器**或**命名空间**。您可以在请求处理过程中**动态地为其添加任何属性**。

#### **常见用法示例**

```python
from flask import Flask, g, request
import sqlite3

app = Flask(__name__)

# 1. 在 before_request 中设置数据库连接
@app.before_request
def before_request():
    # 创建一个数据库连接，并存入 g
    g.db = sqlite3.connect('database.db')
    g.db.row_factory = sqlite3.Row  # 设置返回字典-like 的行

# 2. 在视图函数中使用 g 中的数据
@app.route('/users')
def get_users():
    # 从 g 中获取数据库连接
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return str(users)

# 3. 在 teardown_request 中清理资源
@app.teardown_request
def teardown_request(exception):
    # 检查 g.db 是否存在，然后关闭
    db = g.pop('db', None)
    if db is not None:
        db.close()

# 4. 动态添加其他属性
@app.before_request
def add_user_info():
    # 假设从请求头或 Token 中解析出用户 ID
    user_id = request.headers.get('X-User-ID')
    if user_id:
        g.user_id = int(user_id)  # 动态添加 user_id 属性
        g.is_authenticated = True # 动态添加认证状态

@app.route('/profile')
def profile():
    if hasattr(g, 'is_authenticated') and g.is_authenticated:
        return f"Hello User {g.user_id}"
    else:
        return "Please log in"
```

#### **`g` 对象的内置方法/属性**

虽然 `g` 主要用于存储自定义数据，但它也继承自 `werkzeug.local.LocalProxy`，因此有一些特殊行为：

*   **动态属性**：您可以随时通过 `g.my_variable = value` 来创建新属性。
*   **`g._get_current_object()`**：这是一个底层方法，通常不需要直接调用。它返回 `g` 对象在当前上下文中的实际实例。
*   **`hasattr(g, 'attribute_name')`**：用于检查某个属性是否已设置。
*   **`getattr(g, 'attribute_name', default)`**：安全地获取属性，如果不存在则返回默认值。
*   **`g.pop('attribute_name', default)`**：从 `g` 中移除一个属性并返回其值，如果不存在则返回默认值。常用于清理资源。

---

### **`g` vs `session`**

| 特性 | `g` | `session` |
| :--- | :--- | :--- |
| **生命周期** | 单个请求内 | 跨多个请求（由 Cookie 支持） |
| **存储位置** | 服务器内存（请求上下文中） | 客户端浏览器（Cookie） + 服务器（可选，如 session 存储） |
| **数据持久性** | 请求结束即消失 | 可以持续数小时、数天或永久（“记住我”） |
| **典型用途** | 数据库连接、临时计算结果、请求上下文信息 | 用户登录状态、用户偏好设置 |

---

### **总结**

`g` 对象没有固定的“成员列表”。它的成员是**您在请求处理过程中动态添加的任何属性**。它的主要价值在于提供了一个**请求级别的全局命名空间**，让您可以在同一个请求的不同函数（如 `before_request` 和视图函数）之间方便、安全地共享数据，而无需通过函数参数层层传递。