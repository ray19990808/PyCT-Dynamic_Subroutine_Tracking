import pickle
import os
from myDNN import NNModel 
import open_pkl
import numpy as np
import keras
import itertools
from cal_neuron_coverage import neuron_coverage

if __name__=='__main__':

    folder='/home/soslab/PyCT-optimize/log/ct_log/5_12_mnist_rnn_09650/load_model_testcase.py/predict'
    model_folder_name=folder.split('/')[6]
    model_name=model_folder_name[model_folder_name.find('_',3)+1:]

    model_folder='/home/soslab/PyCT-optimize/model'
    model_path=os.path.join(model_folder,model_name+'.h5')

    model = keras.models.load_model(model_path)
    
    layers = [l for l in model.layers if type(l).__name__ not in ['Dropout']]
    myModel = NNModel()

    # 1: is because 1st dim of input shape of Keras model is batch size (None)
    myModel.input_shape = model.input_shape[1:]
    for layer in layers:
        myModel.addLayer(layer)

    input_shape = myModel.input_shape
    # print("model:",myModel)
    iter_args = (range(dim) for dim in input_shape)
    data=open_pkl.open_pkl(folder)
    input_list=[]
    for arg_tuple in data:
        X = np.zeros(input_shape).tolist()
        data_name_prefix = "v_"
        for i in itertools.product(*iter_args):
            if len(i) == 2:
                X[i[0]][i[1]] = arg_tuple[0][f"{data_name_prefix}{i[0]}_{i[1]}"]
            elif len(i) == 3:
                X[i[0]][i[1]][i[2]] = arg_tuple[0][f"{data_name_prefix}{i[0]}_{i[1]}_{i[2]}"]
            elif len(i) == 4:
                X[i[0]][i[1]][i[2]][i[3]] = arg_tuple[0][f"{data_name_prefix}{i[0]}_{i[1]}_{i[2]}_{i[3]}"]
                
        input_list.append(np.array(X).reshape(1, 28, 28, 1).astype('float32'))
    new_input_tensor=np.stack(input_list)

    print(f"orginal cov:{neuron_coverage(model,[input_list[0]])}")
    print(f"cov after pyct:{neuron_coverage(model,new_input_tensor)}")
    
    # for arg_tuple in data:
    #     print(arg_tuple[0])
    # print(data)

