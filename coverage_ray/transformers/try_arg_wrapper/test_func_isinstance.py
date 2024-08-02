def func_a(v):
    print(v)
    
value = func_a

if isinstance(value, (dict, list, tuple, str, int, float, bool, type(None))):
    print('test')