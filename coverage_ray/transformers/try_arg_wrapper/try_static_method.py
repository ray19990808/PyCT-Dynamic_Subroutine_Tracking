# import inspect

# def wrapper_func(func):
#     def wrapped_func(*args, **kwargs):
#         return func(*args, **kwargs)
    
#     return wrapped_func

# class MyClass:
#     @staticmethod
#     def my_static_method():
#         print("Inside static method")
    
#     def my_method(self):
#         # 通过类名调用静态方法
#         self.my_static_method()
#         # MyClass.my_static_method()

# # 获取类的成员方法
# class_methods = inspect.getmembers(MyClass, inspect.isfunction)

# # 为类方法应用包装器函数
# for func_name, func in class_methods:
#     if func_name == "my_static_method":
#         attr_func = getattr(MyClass, func_name).__func__
#         setattr(MyClass, func_name, wrapper_func(attr_func))

# # 创建类的实例并调用方法
# obj = MyClass()
# obj.my_method()

import inspect

def wrapper_func(func):
    def wrapped_func(*args, **kwargs):
        print("Inside wrapper function")
        return func(*args, **kwargs)
    
    return wrapped_func

class OriginalClass:
    def existing_decorator(func):
        def decorated_func(*args, **kwargs):
            print("Inside existing decorator")
            return func(*args, **kwargs)
        
        return decorated_func
    
    @existing_decorator  # 保留原有的装饰器
    def method1(self):
        print("Inside method1")
    
    @staticmethod
    def method2():
        print("Inside method2")


# 获取包装类的成员方法
class_methods = inspect.getmembers(OriginalClass, inspect.isfunction)

# 为包装类方法应用包装器函数
for func_name, func in class_methods:
    if func_name != "__init__":  # 跳过构造函数
        setattr(OriginalClass, func_name, wrapper_func(func))

# 创建包装类的实例并调用方法
obj = OriginalClass()
# obj.method1()
obj.method2()
