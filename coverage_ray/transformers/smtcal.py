import os
import glob
import pandas as pd

def read_excel_files_from_subfolders(main_folder):
    # 存储读取的数据
    data_frames = []
    exceptions=0
    # 遍历主目录中的所有子目录
    for subfolder_ in os.listdir(main_folder):
        
        subfolder_path = os.path.join(main_folder, subfolder_)
        if os.path.isdir(subfolder_path):
            
            for subfolder in os.listdir(subfolder_path):
                subfolder_path_ = os.path.join(subfolder_path, subfolder)
                
                if os.path.isdir(subfolder_path_):
                    # 查找子目录中的所有符合条件的 Excel 文件
                    for file in glob.glob(os.path.join(subfolder_path_, "*.csv")):
                        # 读取 Excel 文件并添加到列表中
                        df = pd.read_csv(file)
                        data_frames.append(df)
                    for file in glob.glob(os.path.join(subfolder_path_, 'exception.txt')):
                        # 读取 Excel 文件并添加到列表中
                        with open(file, 'r') as f:
                            for line in f:
                                exceptions += line.count('Traceback')

    return data_frames,exceptions

# 主目录路径
main_folder = "/home/soslab/pyct-coverage/coverage_ray/transformers/ct_log/可以用的data/model_inference/7_1"

# 调用函数并获取所有数据
all_data_frames,exceptions = read_excel_files_from_subfolders(main_folder)

# 打印读取的数据（可以根据需要进行进一步处理）
sat=0
unsat=0
timeout=0
for i, df in enumerate(all_data_frames):
    sat+=df.iloc[[0],[1]].sum()
    unsat+=df.iloc[[1],[1]].sum()
    timeout+=df.iloc[[2],[1]].sum()

print(sat)
print(unsat)
print(timeout)
print(exceptions)
