import importlib
import inspect

def run_test_functions(package, module, filename):
    # 动态导入模块
    module_name = f"{package}.{module}.{filename}"
    imported_module = importlib.import_module(module_name)

    # 获取模块中的所有成员
    members = inspect.getmembers(imported_module)

    # 筛选出所有名称中包含 'test' 的函数
    test_functions = [func for name, func in members if inspect.isfunction(func) and name.startswith('test')]

    # 执行所有筛选出的函数
    for func in test_functions:
        print(f"Running {func.__name__}...")
        func()

# 示例用法
run_test_functions('transformers', 'tests', 'test_modeling_flax_common')