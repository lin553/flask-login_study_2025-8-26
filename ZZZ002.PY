# @wraps 装饰器（来自 functools）
# 使用装饰器会改变原函数的一些元数据（如 __name__, __doc__）。@wraps 可以保留这些信息。


from functools import wraps

def my_decorator(func):
    @wraps(func) # 保留原函数的元数据
    def wrapper(*args, **kwargs):
        """Wrapper function docstring."""
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@my_decorator
def example():
    """Example function docstring."""
    pass

print(example.__name__)  # 输出: example (而不是 wrapper)
print(example.__doc__)   # 输出: Example function docstring. (而不是 Wrapper function docstring.)




print("\n\n\n")


# 不 保留元数据
def my_decorator_2(func):
    # @wraps(func) # 保留原函数的元数据
    def wrapper(*args, **kwargs):
        """Wrapper function docstring."""
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@my_decorator_2
def example_2():
    """Example function docstring."""
    pass

print(example_2.__name__)  # 输出: example (而不是 wrapper)
print(example_2.__doc__)   # 输出: Example function docstring. (而不是 Wrapper function docstring.)