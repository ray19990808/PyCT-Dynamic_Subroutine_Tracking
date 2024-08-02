import pickle
import os

def open_pkl(folder_name):
    
    # 打开 .pkl 文件进行读取
    with open(os.path.join(folder_name,'inputs.pkl'), 'rb') as file:
    # with open('/home/soslab/PyCT-optimize/log/ct_log/load_model_testcase.py/predict/inputs.pkl', 'rb') as file:
        # 使用 pickle.load() 反序列化
        data = pickle.load(file)

    # 现在 data 是反序列化后的 Python 对象
    # print(data)
    # for d in data:
    #     print(d[1])
    
    # 有一筆arg是原本的
    print(f"共{len(data)-1}筆new arg")

    return data

if __name__=='__main__':
    open_pkl('/home/soslab/PyCT-optimize/log/ct_log/5_14/myDNN.py/NNModel.layer_forward')

