import os
import sys
import keras
import logging
from myDNN import NNModel 
import traceCall as tc
import numpy as np
import itertools
import cal_neuron_coverage

from utils.pyct_attack_exp_research_question import pyct_mnist_random,pyct_mnist_rnn_random
# from utils.pyct_attack_exp import get_save_dir_from_save_exp
PYCT_ROOT = '/home/soslab/PyCT-optimize'
MODEL_ROOT = os.path.join(PYCT_ROOT, 'model')

myModel=None
myModel2=None
def init_model(model_path):
        global myModel,myModel2
        model = keras.models.load_model(model_path)
        layers = [l for l in model.layers if type(l).__name__ not in ['Dropout']]
        myModel = NNModel()
        myModel2=model

        # 1: is because 1st dim of input shape of Keras model is batch size (None)
        myModel.input_shape = model.input_shape[1:]
        for layer in layers:
            myModel.addLayer(layer)
        
        # print("model:",myModel)
def predict(**data):
        input_shape = myModel.input_shape
        # print("model:",myModel)
        iter_args = (range(dim) for dim in input_shape)
        X = np.zeros(input_shape).tolist()
        data_name_prefix = "v_"
        for i in itertools.product(*iter_args):
            
            if len(i) == 2:
                X[i[0]][i[1]] = data[f"{data_name_prefix}{i[0]}_{i[1]}"]
            elif len(i) == 3:
                X[i[0]][i[1]][i[2]] = data[f"{data_name_prefix}{i[0]}_{i[1]}_{i[2]}"]
            elif len(i) == 4:
                X[i[0]][i[1]][i[2]][i[3]] = data[f"{data_name_prefix}{i[0]}_{i[1]}_{i[2]}_{i[3]}"]

        out_val = myModel.forward(X)
        
        # 用一顆神經元做二分類
        if len(out_val) == 1:
            if out_val[0] > 0.5:
                ret_class = 1
            else:
                ret_class = 0
        else:
            max_val, ret_class = out_val[0], 0
            for i,cl_val in enumerate(out_val):
                if cl_val > max_val:
                    max_val, ret_class = cl_val, i

        logging.info(f"[DEBUG]predicted class:{ret_class}")
        return ret_class

def predict2(**data):
        input_shape = myModel.input_shape
        # print("model:",myModel)
        iter_args = (range(dim) for dim in input_shape)
        X = np.zeros(input_shape).tolist()
        data_name_prefix = "v_"
        for i in itertools.product(*iter_args):
            print(i)
            if len(i) == 2:
                X[i[0]][i[1]] = data[f"{data_name_prefix}{i[0]}_{i[1]}"]
            elif len(i) == 3:
                X[i[0]][i[1]][i[2]] = data[f"{data_name_prefix}{i[0]}_{i[1]}_{i[2]}"]
            elif len(i) == 4:
                X[i[0]][i[1]][i[2]][i[3]] = data[f"{data_name_prefix}{i[0]}_{i[1]}_{i[2]}_{i[3]}"]

        myInput=np.array(X)
        
        myInput = myInput.reshape(1, 28, 28, 1).astype('float32') / 255
        output=myModel2.predict(myInput)
        logging.info(f"try some output: {output}")
        coverage = cal_neuron_coverage.neuron_coverage(myModel2, myInput)
        logging.info("Neuron Coverage: {:.2f}%".format(coverage))
        # 用一顆神經元做二分類
        
        return output

# class load_model_testcase(unittest.TestCase):

#     def test_model_PyCT(self):

#         inputs=[]
#         modelN=[]
#         os.environ['run_pyct_in_unittest'] = 'True'
#         f=open("/home/soslab/PyCT-optimize/model/used_model.txt","r")
        
#         for model_name in f.read().splitlines():
#             # print(f"add {model_name}")
#             inputs.append(pyct_mnist_random(model_name))
#             modelN.append(model_name)
#             # print(inputs)
#         # print(self.modelN)

#         for i,model_name in enumerate(modelN):
            
#             input=inputs[i]
#             model_path = os.path.join(MODEL_ROOT, f"{model_name}.h5")
#             modpath = os.path.join(PYCT_ROOT, f"dnn_predict_common.py")
#             func = "predict"
#             funcname = t if (t:=func) else modpath.split('.')[-1]
#             save_dir = None
#             smtdir = None


#             dump_projstats = False
#             file_as_total = False
#             formula = None
#             include_exception = False
#             lib = None
#             logfile = None
#             # root = os.path.dirname(__file__)
#             root="/home/soslab/PyCT-optimize"
#             safety = 0
#             # verbose = 1 # 5:all, 3:>=DEBUG. 2:including SMT, 1: >=INFO
#             # norm = True


#             statsdir = None
#             if dump_projstats:
#                 statsdir = os.path.join(
#                     os.path.abspath(os.path.dirname(__file__)), "project_statistics",
#                     os.path.abspath(root).split('/')[-1], modpath, funcname)

#             # from libct.utils import get_module_from_rootdir_and_modpath, get_function_from_module_and_funcname
#             # module = get_module_from_rootdir_and_modpath(root, modpath)
#             # func_init_model = get_function_from_module_and_funcname(module, "init_model")
#             # execute = get_function_from_module_and_funcname(module, funcname)
#             # func_init_model(model_path) #dnn_predict_common_line9
#             # execute(**input[0]['in_dict'])
#             #----- build model finish!!-----
#             # print(input[0]['in_dict'])

#             i=predict(init_model(model_path),input[0]['in_dict'])
            
#             print(i)

def test_model_PyCT():
    inputs=[]
    modelN=[]
    os.environ['run_pyct_in_unittest'] = 'True'
    f=open("/home/soslab/PyCT-optimize/model/used_model.txt","r")
    
    # for model_name in f.read().splitlines():
    #     modelN.append(model_name)

    # for i,model_name in enumerate(modelN):
    
    # only use one model

    # 記得整理log資料夾！！！！！！！！！！
    # model_name='mnist_sep_act_m6_9628'
    # model_name='mnist_sep_act_m6_9653_noise'
    # model_name='mnist_sep_act_m7_9876'
    # model_name='simple_mnist_bad_07685'
    model_name='simple_mnist_m6_09585'
    # model_name='mnist_rnn_09650'

    if model_name in ['mnist_sep_act_m6_9628','mnist_sep_act_m6_9653_noise','mnist_sep_act_m7_9876','simple_mnist_bad_07685','simple_mnist_m6_09585']:
        input=pyct_mnist_random(model_name)
    elif model_name in ['mnist_rnn_09650']:
        input=pyct_mnist_rnn_random(model_name)
    model_path = os.path.join(MODEL_ROOT, f"{model_name}.h5")
    modpath = os.path.join(PYCT_ROOT, f"dnn_predict_common.py")
    func = "predict"
    funcname = t if (t:=func) else modpath.split('.')[-1]
    save_dir = None
    smtdir = None


    dump_projstats = False
    file_as_total = False
    formula = None
    include_exception = False
    lib = None
    logfile = None
    # root = os.path.dirname(__file__)
    root="/home/soslab/PyCT-optimize"
    safety = 0
    # verbose = 1 # 5:all, 3:>=DEBUG. 2:including SMT, 1: >=INFO
    # norm = True


    # from libct.utils import get_module_from_rootdir_and_modpath, get_function_from_module_and_funcname
    # module = get_module_from_rootdir_and_modpath(root, modpath)
    # func_init_model = get_function_from_module_and_funcname(module, "init_model")
    # execute = get_function_from_module_and_funcname(module, funcname)
    # func_init_model(model_path) #dnn_predict_common_line9
    # execute(**input[0]['in_dict'])
    #----- build model finish!!-----
    # print(input[0]['in_dict'])
    

    init_model(model_path)
    sys.setprofile(tc.trace_calls)
    
    i=predict(**input[0]['in_dict'])

    # predict2(**input[0]['in_dict'])
    sys.setprofile(None)

    # print(function_list)
    # with open('/home/soslab/PyCT-optimize/function_list.txt', 'w') as f:
    #     # 对于列表中的每个值，将其写入文件并添加换行符
    #     for item in function_list:
    #         print("!!")
    #         f.write(f"{item}\n")  # 写入列表中的项，换行


if __name__ == '__main__': 
    
    # b=load_model_testcase()
    # b.test_model_PyCT()
    # FORMAT = '%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s'
    logging.basicConfig(level=logging.INFO)
    test_model_PyCT()
    
    # unit_test.unit_test('test_modeling_albert')
    






#     os.environ['run_pyct_in_unittest'] = 'True'
#     cov = coverage.Coverage()
#     cov.start() # Start measuring coverage
#     loader = unittest.TestLoader()
#     # suite = loader.discover(start_dir='.', pattern=pattern)
#     suite = loader.discover(start_dir='.', pattern='load_model_testcase.py')
#     runner = unittest.TextTestRunner(verbosity=1)


#     runner.run(suite)
    
#     cov.stop() # Stop measuring coverage
#     cov.save() # Save the coverage data to disk
#     cov.report(skip_empty=True,show_missing=True,file=open(f'coverage_report_manual/unittest.txt', 'w'))
