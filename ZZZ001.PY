# 带参数的装饰器
# 装饰器本身也可以接收参数，这需要再嵌套一层函数。


def repeat(n): # 装饰器工厂函数，接收参数 n
    def decorator(func): # 真正的装饰器
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator # 返回装饰器函数

@repeat(3) # 调用 repeat(3) 返回一个装饰器，然后用这个装饰器去装饰 say_hi
def say_hi():
    print("Hi!")

say_hi()
# 输出：
# Hi!
# Hi!
# Hi!