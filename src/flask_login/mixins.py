class UserMixin:
    """
    This provides default implementations for the methods that Flask-Login
    expects user objects to have.
    
    此类为 Flask-Login 所期望用户对象具备的方法提供了默认实现。
    """

    # Python 3 implicitly set __hash__ to None if we override __eq__
    # We set it back to its default implementation
    # 如果我们重写了 __eq__，Python 3 会隐式地将 __hash__ 设为 None
    # 我们将其恢复为默认实现
    __hash__ = object.__hash__

    @property
    def is_active(self):
        """
        Returns `True` if the user is active (authenticated and allowed to log in).
        默认返回 `True`，表示用户是活跃的。
        """
        return True

    @property
    def is_authenticated(self):
        """
        Returns `True` if the user is authenticated (logged in).
        如果用户已通过身份验证（已登录），则返回 `True`。
        """
        return self.is_active

    @property
    def is_anonymous(self):
        """
        Returns `False` for a regular user (not anonymous).
        对于普通用户（非匿名），返回 `False`。
        """
        return False

    def get_id(self):
        """
        Returns a unique identifier for the user as a string.
        以字符串形式返回用户的唯一标识符。
        
        :raises NotImplementedError: If the `id` attribute is not present.
        :raises NotImplementedError: 如果 `id` 属性不存在。
        """
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    def __eq__(self, other):
        """
        Checks the equality of two `UserMixin` objects using `get_id`.
        
        使用 `get_id` 检查两个 `UserMixin` 对象是否相等。
        
        :param other: Another object to compare with.
        :param other: 另一个要比较的对象。
        :return: `True` if both objects have the same ID, `False` otherwise.
        :return: 如果两个对象具有相同的 ID，则返回 `True`，否则返回 `False`。
        """
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        
        # NotImplemented 既不是 True 也不是 False。它是一个特殊的单例对象（Singleton Object），用于表示“未实现”或“无法比较”。
        return NotImplemented       

    def __ne__(self, other):
        """
        Checks the inequality of two `UserMixin` objects using `get_id`.
        
        使用 `get_id` 检查两个 `UserMixin` 对象是否不相等。
        
        :param other: Another object to compare with.
        :param other: 另一个要比较的对象。
        :return: `True` if both objects have different IDs, `False` otherwise.
        :return: 如果两个对象具有不同的 ID，则返回 `True`，否则返回 `False`。
        """
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


class AnonymousUserMixin:
    """
    This is the default object for representing an anonymous user.
    
    这是表示匿名用户的默认对象。
    """

    @property
    def is_authenticated(self):
        """
        Returns `False` for an anonymous user (not logged in).
        对于匿名用户（未登录），返回 `False`。
        """
        return False

    @property
    def is_active(self):
        """
        Returns `False` for an anonymous user (not active).
        对于匿名用户（非活跃），返回 `False`。
        """
        return False

    @property
    def is_anonymous(self):
        """
        Returns `True` for an anonymous user.
        对于匿名用户，返回 `True`。
        """
        return True

    def get_id(self):
        """
        Returns `None` for an anonymous user (no ID).
        对于匿名用户（无 ID），返回 `None`。
        """
        return None