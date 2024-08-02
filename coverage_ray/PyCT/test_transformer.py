# git clone -b "v4.28.1" --single-branch https://github.com/huggingface/transformers.git
# ver = 4.28.1
# pip install transformer

from libct.utils import get_module_from_rootdir_and_modpath
from libct.utils import get_function_from_module_and_funcname
import func_timeout, inspect

rootdir = "/home/jack/coverage/PyCT/transformers/src/transformers"
modpath = "utils.logging"

mod = func_timeout.func_timeout(10, get_module_from_rootdir_and_modpath, args=(rootdir, modpath,))
ans = []
tmp = inspect.getmembers(mod)

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

print(ans)