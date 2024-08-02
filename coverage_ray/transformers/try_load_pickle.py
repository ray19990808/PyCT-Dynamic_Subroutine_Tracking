# import pickle
import os

# with open("arg_type.pickle", "rb") as f:
#     arg_type = pickle.load(f)

if os.path.exists("error_func_list.txt"):
    with open('error_func_list.txt', 'r') as f:
        error_func_list = f.read().splitlines()
        filter_set = set(error_func_list)
        
print(filter_set)

with open("error_func_list.txt", "w") as f:
    filter_set = list(filter_set)
    for i in range(len(filter_set)):
        filter_set[i] = filter_set[i] + "\n"
    f.writelines(filter_set)

