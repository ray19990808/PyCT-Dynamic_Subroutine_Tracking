import sys
import inspect
import os
import logging
import json
from try_run_pyct import pyct_test_transformers
import random
import numpy as np
import json
import os

def check_and_append_json(A):
    """
    Check if the string A is in the JSON file file_B, if not, append A to file_B.
    
    Args:
    A (str): The string to check and append.
    file_B (str): The path to the JSON file to check and append the string to.
    """
    data = []
    
    # Check if the file exists
    if os.path.exists('/home/soslab/pyct-coverage/coverage_ray/transformers/wrapped_fun.json'):
        # Read the existing data from the JSON file
        with open('/home/soslab/pyct-coverage/coverage_ray/transformers/wrapped_fun.json', 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                # Handle the case where the file is empty or corrupted
                pass
    else:
        with open('/home/soslab/pyct-coverage/coverage_ray/transformers/wrapped_fun.json', 'w') as f:
            pass
    
    # Check if A is in the data
    if A not in data:
        data.append(A)
        # Write the updated data back to the JSON file
        with open('/home/soslab/pyct-coverage/coverage_ray/transformers/wrapped_fun.json', 'w') as f:
            json.dump(data, f, indent=4)
    else:
        return True
    
    return False



def trace_calls(frame, event, arg):
    DISALLOWED_FUNCTIONS = {'__init__', 'getstate', 'decode','_shutdown','actFunc','unit_test','__exit__','__setattr__','walk'}
    DISALLOWED_FUNCTIONS_OURS = {'/lib/python3.8/logging','/lib/python3.8/multiprocessing','/lib/python3.8/ast','/site-packages/_pytest','/site-packages/pytest'
                                 '/lib/python3.8/threading','/lib/python3.8/unittest','/lib/python3.8/site-packages/coverage',
                                 '/lib/python3.8/coverage','/lib/python3.8/site-packages/coverage','/lib/python3.8/re','/lib/python3.8/sre',
                                 '/lib/python3.8/posixpath','/lib/python3.8/weakref.py','/lib/python3.8/os','/lib/python3.8/enum','/lib/python3.8/contextlib'}

    
    sys.setprofile(None)
    if event == 'call':
        function_name = frame.f_code.co_name
        file_path = frame.f_code.co_filename
        full_path = os.path.abspath(file_path)

        # 检查函数名是否在允许列表中
        if function_name in DISALLOWED_FUNCTIONS or function_name.startswith('_'):
            sys.setprofile(trace_calls)
            return trace_calls
        
        for df in DISALLOWED_FUNCTIONS_OURS:
            
            if df in full_path:
                sys.setprofile(trace_calls)
                return trace_calls

        if check_and_append_json(f'{function_name} in {full_path}'):
            sys.setprofile(trace_calls)
            return trace_calls
        
        logging.info(f"當前函數: {function_name}")
        func = frame.f_globals.get(function_name)
        # print(f"globals:{frame.f_globals}\n")
        # print(f"locals:{frame.f_locals}\n")
        if func is None:
            func = frame.f_locals.get(function_name)

        current_frame = frame
        if func is None:
            while current_frame.f_back is not None:
                current_frame = current_frame.f_back
                if function_name in current_frame.f_locals:
                    func=current_frame.f_locals.get(function_name)
                if function_name in current_frame.f_globals:
                    func=current_frame.f_globals.get(function_name)
        
        for name, value in frame.f_globals.items():
            # 确保这是一个对象并且有属性
            if inspect.isclass(value) and hasattr(value,function_name):
                func=getattr(value,function_name)

        if func is None:
            logging.info(f"無法調用該函数 {function_name}")
        else: 
            try:
                input_values = frame.f_locals
                
                logging.debug(f"input為: ({input_values.items()}, callable:{callable(func)})")
                if input_values.items()!={}.items() and callable(func):
                    
                    
                    logging.info(f"full_path:{full_path}")
                    # module_name = os.path.splitext(os.path.basename(file_path))[0]
                    # 获取函数的签名
                    sig = inspect.signature(func)
                    local_vars = dict(frame.f_locals.items())
                    # 构建参数字典，包含普通参数和 `**kwargs`
                    # print(f"sig.parameters:{sig.parameters}")
                    # for key in sig.parameters:
                    #     print(key)
                    #     print(f"sig.parameters[key].kind:{sig.parameters[key].kind}")
                    #     print(key in local_vars,"\n")
                    
                    

                    # positional_or_keyword_args = {
                    #     key: local_vars[key] for key in sig.parameters 
                    #     if sig.parameters[key].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
                    # }

                    positional=tuple()

                    # process POSITIONAL_OR_KEYWORD
                    for key in sig.parameters: 
                        if sig.parameters[key].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                            positional+=(local_vars[key],)
                    # logging.debug(f"positional_or_keyword_args:",*positional)
                    # var_positional_args=tuple()

                    # process VAR_POSITIONAL
                    for key in sig.parameters:
                        
                        if sig.parameters[key].kind == inspect.Parameter.VAR_POSITIONAL:
                            for arg in local_vars[key]:
                                positional+=(arg,)
                                # print(var_positional_args)
                            
                    # logging.debug(f"positional_or_keyword_args & var_positional_args:",*positional)
                    
                    # 获取 VAR_KEYWORD 参数 (**kwargs)
                    var_keyword_args={}
                    
                    for key in sig.parameters:
                        if sig.parameters[key].kind == inspect.Parameter.VAR_KEYWORD:
                            var_keyword_args[key]=local_vars[key]
                        # print(var_keyword_args)
                    # var_keyword_args = {
                    #     key: local_vars[key] for key in sig.parameters 
                    #     if sig.parameters[key].kind == inspect.Parameter.VAR_KEYWORD
                    # }
                    # logging.debug(f"var_keyword_args:",var_keyword_args)
                    

                    # 获取 KEYWORD_ONLY 参数
                    keyword_only_args = {
                        key: local_vars[key] for key in sig.parameters 
                        if sig.parameters[key].kind == inspect.Parameter.KEYWORD_ONLY
                    }
                    # logging.debug(f"keyword_only_args:",keyword_only_args)
                    all_kwargs={}
                    all_kwargs.update(keyword_only_args) 
                    for key,value in var_keyword_args.items():
                        all_kwargs.update(**var_keyword_args[key])
                    logging.debug(f"all_kwargs:{all_kwargs}")
                    # 重新调用函数
                    # print(f"input:{input_values.items()}")
                    
                    # check function running
                    # print(f"run function in call:{func(*positional, **all_kwargs)}")

                    run_function_with_pyct(func,full_path,*positional,**all_kwargs)
                    logging.info(f"[Wrap Import Method] {function_name} in {full_path} process complete")
                else:
                    logging.info(f"{function_name} 沒有參數不執行pyct") 
                # else:
                    
                #     print(f"result:{func()}") 
            except AttributeError as e:
                logging.info(f"some AttributeError error:{e}")
            except AssertionError as e:
                logging.info(f"some assertion error:{e}")
            except Exception as e:
                logging.info(e)
            # for key, value in input_values.items():
            #     print(f"Key: {key}, Value: {value}")

    sys.setprofile(trace_calls)
    return trace_calls

def run_function_with_pyct(func,full_path,*args,**kwargs):
    module_name = func.__module__
    func_name = func.__qualname__  
    # print("arg: ",args)
    # if not module_name.startswith("unittest.case"):
        # file = inspect.getfile(func)
    file=full_path
    logging.info(f"file:{file},func:{func_name}")
    in_dict = dict()
    params = inspect.signature(func).parameters.items()
    
    can_concolic = False
    primitive_type = (bool, float, int, str)
    # primitive_type = (bool, float, int)
    primitive_args = dict()
    for i, ((p_name, p_obj), arg) in enumerate(zip(params, args)):
        logging.debug(f"param: {((p_name, p_obj), type(arg))} ,kind: {p_obj.kind}")
        if p_obj.kind == inspect.Parameter.VAR_POSITIONAL:
            # *args,VAR_POSITIONAL
            in_dict["*args"] = []
            primitive_args["*args"] = []
            
            for arg in args[i:]:
                logging.debug(f"checking {arg} in *args(VAR_POSITIONAL)")
                if type(arg) in primitive_type:
                    can_concolic = True
                    primitive_args["*args"].append(arg)
                else:
                    primitive_args["*args"].append("NOT_PRIMITIVE")
                
                in_dict["*args"].append(arg)
            
            break
                        
        if type(arg) in primitive_type:
            logging.debug(f"checking {arg} (POSITIONAL_OR_KEYWORD)")
            primitive_args[p_name] = arg
            can_concolic = True
        else:
            if type(arg) in 
            logging.debug(f"checking {arg} (POSITIONAL_OR_KEYWORD)")
            primitive_args[p_name] = "NOT_PRIMITIVE"

        in_dict[p_name] = arg

    for p_name, arg in kwargs.items():
        logging.debug(f"checking {arg} in **kwargs")
        if type(arg) in primitive_type:
            primitive_args[p_name] = arg
            can_concolic = True
        else:
            logging.debug(f"arg:{arg} not promitive")
            primitive_args[p_name] = "NOT_PRIMITIVE"
        
        in_dict[p_name] = arg
    logging.info(f"{module_name}.{func_name} is called and can_concolic :{can_concolic}")
    logging.debug(f"in_dict: {in_dict}")
    #logging.info(f"{module_name}.{func_name} is called and can_concolic :{can_concolic} ,func_name not in skip_func_list :{func_name not in skip_func_list}")
    if can_concolic:
        #小呆節省效能用
        history = dict()
        if os.path.exists('/home/soslab/pyct-coverage/coverage_ray/transformers/can_fork_pyct_func.json'):
            with open('/home/soslab/pyct-coverage/coverage_ray/transformers/can_fork_pyct_func.json', 'r') as f:
                history = json.load(f)
    
        if file not in history:
            history[file] = dict()

        #print(f"{func_name} can_concolic, not in skip_func_list, not in history: {func_name not in history[file]}")
        
        if func_name not in history[file]:
            history[file][func_name] = primitive_args
            with open('/home/soslab/pyct-coverage/coverage_ray/transformers/can_fork_pyct_func.json', 'w') as f:
                json.dump(history, f, indent='\t')
        else:
            logging.info(f"{module_name}.{func_name} has been processed by pyct")
            return

        
        logging.info('@' * 100)
        logging.info(f"this function can use concolic testing:{module_name}.{func_name}")
        # logging.info(f"primitive_args:")
        # logging.info(json.dumps(primitive_args, indent='\t'))
        # print("="*15,f"this function can use concolic testing:{module_name}.{func_name}", "="*15)
        
        pyct_test_transformers(file, func_name, in_dict,_func=func)

def fuzzing_function(func, input_data):
    
    def fuzz_value(value):
        """对单个值进行模糊测试"""
        if isinstance(value, int):
            return random.randint(0, 100)
        elif isinstance(value, float):
            return random.uniform(0.0, 100.0)
        elif isinstance(value, str):
            return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=len(value)))
        elif isinstance(value, bool):
            return not value
        else:
            return value
    
    original_output=func(input_data)
    if isinstance(input_data, tuple):
        fuzzed_input = (fuzz_value(input_data[0]),) + input_data[1:]
    elif isinstance(input_data, list):
        fuzzed_input = [fuzz_value(input_data[0])] + input_data[1:]
    elif isinstance(input_data, np.ndarray):
        fuzzed_input = input_data.copy()
        fuzzed_input[0] = fuzz_value(fuzzed_input[0])
    else:
        raise ValueError("Input data must be of type tuple, list, or ndarray.")
    
    for i in range(10):
        try:
            if func(fuzzed_input)!=original_output:
                return fuzzed_input
        except:
            return fuzzed_input
    return fuzzed_input

def wrap_function(wrapper_func,module_name,func_name, func):
    
    # relpath = os.path.relpath(inspect.getfile(module), os.getcwd())
    realpath = None
    try:
        module=_get_module_from_name(module_name)
        relpath = os.path.relpath(inspect.getfile(module), os.getcwd())
    except Exception as e:
        logging.info(f"[ERROR]: Cannot get relpath maybe it is built-in function:{e}")
        return
    
    setattr(module, func_name, wrapper_func(func))

def _get_module_from_name(name):
    __import__(name)
    return sys.modules[name]


# def trace_calls(frame, event, arg):
#     if event == 'call':
#         function_name = frame.f_code.co_name
#         print(f"调用了函数1: {function_name}")
#         func = frame.f_globals.get(function_name)
        
#         if func is None:
#             func = frame.f_locals.get(function_name)
#         if func is None:
#             print(f"目前找不到函数 {function_name}")
#         else: print(f"调用了函数2: {func}")
#         if callable(func):
#             print("!!!")
            
#     return trace_calls