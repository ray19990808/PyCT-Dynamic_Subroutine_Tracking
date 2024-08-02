import coverage
import multiprocessing
import os
import time
from pathlib import Path

from to_be_imported import *
from pathlib import Path
import pyct


verbose = 3


def extract_function_list_from_modpath(rootdir, modpath):
    ans = []; print(modpath, '(' + modpath.replace('.', '/') + '.py)', '==> ', end='')
    if modpath.endswith('.__init__'): return ans # an empty list here
    try:
        # mod = func_timeout.func_timeout(10, get_module_from_rootdir_and_modpath, args=(rootdir, modpath,))
        mod = get_module_from_rootdir_and_modpath(rootdir, modpath)
        print(mod, end='')
        for _, obj in inspect.getmembers(mod):
            try:
                inspect.isclass(obj)
            except:
                continue
            
            if inspect.isclass(obj):
                for _, o in inspect.getmembers(obj):
                    if (inspect.isfunction(o) or inspect.ismethod(o)) and o.__module__ == modpath: # and inspect.signature(o).parameters:
                        ans.append(o.__qualname__)#; print(o.__qualname__)
            elif (inspect.isfunction(obj) or inspect.ismethod(obj)) and obj.__module__ == modpath: # and inspect.signature(obj).parameters:
                ans.append(obj.__qualname__)#; print(obj.__qualname__)
        i = 0
        while i < len(ans):
            if '<locals>' in ans[i]: del ans[i]; continue # cannot access nested functions
            if get_function_from_module_and_funcname(mod, ans[i], True) is None: del ans[i]; continue # similar to assert
            if len(ans[i].split('.')) == 2:
                (a, b) = ans[i].split('.')
                if b.startswith('__') and not b.endswith('__'): b = '_' + a + b
                ans[i] = a + '.' + b
            i += 1
    except func_timeout.FunctionTimedOut: pass
    except Exception as e:
        print('Exception: ' + str(e), end='', flush=True)
        import traceback; traceback.print_exc()
        
        print('cannot get_module_from_rootdir_and_modpath')
        print(rootdir, modpath)
        print("=" * 40)
        
        
        # print('\nWe\'re going to get stuck here...', flush=True)
        # while True: pass
        
        # if 'No module named' in str(e):
        #     print(' Raise Exception!!!', end='')
        #     raise e
    print()
    return ans



def run_pyct(rootdir, files, lib, TOTAL_TIMEOUT, verbose):
    cov = coverage.Coverage() # Create a coverage instance
    cov.load()
    
    for i, file in enumerate(files):
        relative_modpath = str(file.relative_to(rootdir).with_suffix(''))
        relative_modpath = relative_modpath.replace('/', '.')
        
        funcs = extract_function_list_from_modpath(rootdir, relative_modpath)
        
        
        cmd = f"'{rootdir}' '{relative_modpath}' "
        for f in funcs:
            print(f"**********  {cmd} '{f}'")

            cov.start() # Start measuring coverage
            pyct.run(root=rootdir, modpath=relative_modpath, funcname=f,
                    in_dict={}, lib=lib, total_timeout=TOTAL_TIMEOUT, verbose=verbose,)
            cov.stop() # Stop measuring coverage
            try:
                cov.report(file=open('test_coverage_report.txt', 'w'), show_missing=True, omit=['.venv/*', 'libct/*', 'pyct.py'])
            except coverage.exceptions.NoDataError:
                pass
            except Exception as e:
                print(e)

            print('#' * 60)
        
        # 合并子进程的覆盖率数据到共享对象
        cov.save()

  
def test_run_pyct_one_func(rootdir, file, funcname, lib, TOTAL_TIMEOUT, verbose, in_dict):
    cov = coverage.Coverage() # Create a coverage instance
    cov.load()
    
    rootdir = Path(rootdir)
    file = Path(file)
    relative_modpath = str(file.relative_to(rootdir).with_suffix(''))
    relative_modpath = relative_modpath.replace('/', '.')
    
    cmd = f"'{rootdir}' '{relative_modpath}' "
    
    print(f"**********  {cmd} '{funcname}'")

    cov.start() # Start measuring coverage
    pyct.run(root=rootdir, modpath=relative_modpath, funcname=funcname,
            in_dict=in_dict, lib=lib, total_timeout=TOTAL_TIMEOUT, verbose=verbose,)
    cov.stop() # Stop measuring coverage
    # 合并子进程的覆盖率数据到共享对象
    cov.save()
    
    try:
        cov.report(file=open('test_coverage_report.txt', 'w'), show_missing=True, omit=['.venv/*', 'libct/*', 'pyct.py'])
    except coverage.exceptions.NoDataError:
        pass
    except Exception as e:
        print(e)

    print('#' * 60)
    
    
def run_pyct_one_func(rootdir, file, funcname, lib, TOTAL_TIMEOUT, verbose, in_dict):
    rootdir = Path(rootdir)
    file = Path(file)
    relative_modpath = str(file.relative_to(rootdir).with_suffix(''))
    relative_modpath = relative_modpath.replace('/', '.')
    
    cmd = f"'{rootdir}' '{relative_modpath}' "
    
    print(f"[run_pyct_one_func] **********  {cmd} '{funcname}'")

    cov = coverage.Coverage() # Create a coverage instance
    cov.load()
    cov.start() # Start measuring coverage
    pyct.run(root=rootdir, modpath=relative_modpath, funcname=funcname,
            in_dict=in_dict, lib=lib,
            single_timeout=600, total_timeout=TOTAL_TIMEOUT, timeout=TOTAL_TIMEOUT, verbose=verbose,)
    cov.stop() # Stop measuring coverage
    cov.save() # 合并子进程的覆盖率数据到共享对象

    print('#' * 60)
    

def run_pyct_one_func_no_coverage(rootdir, file, funcname, lib, TOTAL_TIMEOUT, verbose, in_dict):
    rootdir = Path(rootdir)
    file = Path(file)
    relative_modpath = str(file.relative_to(rootdir).with_suffix(''))
    relative_modpath = relative_modpath.replace('/', '.')
    
    cmd = f"'{rootdir}' '{relative_modpath}' "
    
    print(f"[run_pyct_one_func_no_coverage] **********  {cmd} '{funcname}'")

    pyct.run(root=rootdir, modpath=relative_modpath, funcname=funcname,
            in_dict=in_dict, lib=lib,
            single_timeout=TOTAL_TIMEOUT, total_timeout=TOTAL_TIMEOUT, timeout=TOTAL_TIMEOUT, verbose=verbose,)

    print('#' * 60)
    exit(0)
    
    
def main(rootdir, pattern, lib, TOTAL_TIMEOUT, verbose, num_processes):
    start = time.time()
    
    # 创建共享的 coverage.Coverage() 对象
    cov = coverage.Coverage()
    
    # 启动数据收集
    cov.start()
    
    processes = []
    
    # 获取所有的 .py 文件
    py_files = list(Path(os.path.join(rootdir, pattern)).rglob('*.py'))
    
    # 平均分配任务
    files_per_process = len(py_files) // num_processes
    
    for i in range(num_processes):
        start_idx = i * files_per_process
        end_idx = (i + 1) * files_per_process if i != num_processes - 1 else None
        assigned_files = py_files[start_idx:end_idx]
        
        p = multiprocessing.Process(target=run_pyct, args=(rootdir, assigned_files, lib, TOTAL_TIMEOUT, verbose))
        p.start()
        processes.append(p)
    
    
    for p in processes:
        p.join()
        

    # 停止数据收集
    cov.stop()
    
    # 生成覆盖率报告
    cov.load()
    cov.report(file=open('test_coverage_report.txt', 'w'), show_missing=True, omit=['.venv/*', 'libct/*', 'pyct.py'])
    
    end = time.time()
    print("Total execution time:", end - start)




if __name__ == '__main__':    
    os.system(f"rm -rf './project_statistics/{project_name}'")
    os.makedirs(os.path.join("project_statistics", project_name))

    if os.path.exists('.coverage'):
        os.remove('.coverage')

    for dirpath, _, _ in os.walk(rootdir):
        dirpath = os.path.abspath(dirpath)
        if dirpath != rootdir and not dirpath.startswith(rootdir + '/.') and '__pycache__' not in dirpath: # and '.venv' not in dirpath:
            # print(dirpath)
            os.system(f"touch '{dirpath}/__init__.py'")
    
    pattern = args.target_dir
    verbose = 3
    num_processes = 1

    main(rootdir, pattern, lib, TOTAL_TIMEOUT, verbose, num_processes)
