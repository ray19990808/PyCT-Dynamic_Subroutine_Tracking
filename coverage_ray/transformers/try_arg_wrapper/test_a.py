# 一定要在最一開始import此模組，後續取得自動import的模組清單才不會錯
import sys
sys.path.insert(0, '/home/jack/mylib')
import arg_wrapper.arg_wrapper as arg_wrapper

import d
from b import *
import sys
import inspect
BUILT_IN_DIR = ['__builtins__', '__cached__', '__doc__',
                '__file__', '__loader__', '__name__', '__package__', '__spec__']


def test_bc():
    print(add(5, 1))
    print(sub(3, 2))
    print(mul(4, 2))
    d.pstr("Hello World")
    obj_func(TestAdd(1, 2))


# 所有被 import 的模組
imported_modules = dict()

# 遍歷所有模組
for module_name, module in sys.modules.items():
    if module and not module.__name__.startswith('builtins') and not module_name in arg_wrapper.auto_imported_modules:
        if hasattr(module, '__file__'):
            imported_modules[module_name] = module
        elif module_name not in sys.builtin_module_names:
            imported_modules[module_name] = module

print(list(imported_modules.keys()))

# 對所有import的模組的所有函式進行包裝
for module_name, module in imported_modules.items():
    for func_name, func in inspect.getmembers(module, inspect.isfunction):
        print(f"{module_name}.{func_name} has been wrapped")
        setattr(module, func_name, arg_wrapper.get_args_types(func))

# 對此模組的所有函式進行包裝
this_module = sys.modules[__name__]
for func_name, func in inspect.getmembers(this_module, inspect.isfunction):
    print(f"{__name__}.{func_name} has been wrapped")
    setattr(this_module, func_name, arg_wrapper.get_args_types(func))

test_bc()
