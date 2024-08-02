import sys
sys.path.insert(0, '/home/jack/mylib')

import arg_wrapper.arg_wrapper as arg_wrapper
import inspect


class Test:
    def __init__(self, a=10):
        self.a = a
    

class_obj = Test
class_obj()
class_methods = inspect.getmembers(class_obj, inspect.isfunction)
for func_name, func in class_methods:
    print(f"[Wrap Class Method] {func_name} has been wrapped")
    setattr(class_obj, func_name, arg_wrapper.get_args_types(func))

print()
class_obj()
