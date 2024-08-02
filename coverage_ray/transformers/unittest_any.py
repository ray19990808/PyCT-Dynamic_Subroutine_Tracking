import os
import sys
# sys.path.insert(0,os.path.dirname(os.getcwd()))
# sys.path.insert(0,'/home/soslab/pyct-coverage')
import unittest
import openai

import time
import logging
# import tensorflow as tf
import anthropic
import coverage

import traceCall as tc

def unit_test(pattern,dir):
    
    
    time_result = time.localtime(time.time())
    time_=f'{time_result.tm_mon}_{time_result.tm_mday}'

    cov = coverage.Coverage(auto_data=True)
    cov.start() # Start measuring coverage
    # os.chdir(dir)
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=dir, pattern=pattern)
    runner = unittest.TextTestRunner(verbosity=1)
    
    # sys.setprofile(tc.trace_calls)
    runner.run(suite)
    # sys.setprofile(None)
    
    cov.stop() # Stop measuring coverage
    cov.save() # Save the coverage data to disk
    # cov.html_report(directory=f'ct_log/{time_}/cov_report',title=f'{pattern}')
    cov.report(file=open(f'/home/soslab/pyct-coverage/coverage_ray/transformers/ct_log/{time_}_{pattern}.txt','w'),ignore_errors=True)
    

    return

def unit_pytest(pattern,dir):
    
    
    time_result = time.localtime(time.time())
    time_=f'{time_result.tm_mon}_{time_result.tm_mday}'

    cov = coverage.Coverage(data_file='/home/soslab/pyct-coverage/coverage_ray/transformers/.coverage',auto_data=True)
    cov.start() # Start measuring coverage
    import pytest

    
    
    sys.setprofile(tc.trace_calls)
    pytest.main([dir])
    sys.setprofile(None)
    
    cov.stop() # Stop measuring coverage
    cov.save() # Save the coverage data to disk
    # cov.html_report(directory=f'ct_log/{time_}/cov_report',title=f'{pattern}')
    cov.report(file=open(f'/home/soslab/pyct-coverage/coverage_ray/transformers/ct_log/{time_}_{pattern}.txt','w'),ignore_errors=True)
    

    return

def program_test():
    
    
    time_result = time.localtime(time.time())
    time_=f'{time_result.tm_mon}_{time_result.tm_mday}'

    cov = coverage.Coverage(data_file='/home/soslab/pyct-coverage/coverage_ray/transformers/.coverage',auto_data=True)
    cov.start() # Start measuring coverage
    # os.chdir(dir)
    
    import numpy as np
    from tensorflow.keras.datasets import mnist
    from tensorflow.keras.models import load_model
    from tensorflow.keras.utils import to_categorical

    # 下載並加載 MNIST 數據集
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # 資料預處理
    x_test = x_test.astype('float32') / 255.0
    x_test = np.expand_dims(x_test, -1)  # 添加一個維度以匹配模型的輸入形狀
    y_test = to_categorical(y_test, 10)  # One-hot 編碼

    # 載入預訓練模型
    model = load_model('/home/soslab/pyct-coverage/coverage_ray/transformers/model/simple_mnist_m6_09585.h5')

    # 使用模型進行預測
    sys.setprofile(tc.trace_calls)
    predictions = model.predict(x_test)
    sys.setprofile(None)
    # 將預測結果轉換為數字
    predicted_labels = np.argmax(predictions, axis=1)
    true_labels = np.argmax(y_test, axis=1)

    # 計算準確率
    accuracy = np.mean(predicted_labels == true_labels)
    

    
    
    
    
    print(f'Accuracy: {accuracy:.4f}')
    cov.stop() # Stop measuring coverage
    cov.save() # Save the coverage data to disk
    # cov.html_report(directory=f'ct_log/{time_}/cov_report',title=f'{pattern}')
    cov.report(file=open(f'/home/soslab/pyct-coverage/coverage_ray/transformers/ct_log/{time_}_program.txt','w'),ignore_errors=True)
    

    return

def chatGPT_test():
    

    time_result = time.localtime(time.time())
    time_=f'{time_result.tm_mon}_{time_result.tm_mday}'

    cov = coverage.Coverage(data_file='/home/soslab/pyct-coverage/coverage_ray/transformers/.coverage',auto_data=True)
    cov.start() # Start measuring coverage
    # os.chdir(dir)

    
    initial_q='How are you?'
    sys.setprofile(tc.trace_calls)
    answer = ask_chatgpt(initial_q)
    sys.setprofile(None)

    print("ChatGPT 的回答是：", answer)
    cov.stop() # Stop measuring coverage
    cov.save() # Save the coverage data to disk
    # cov.html_report(directory=f'ct_log/{time_}/cov_report',title=f'{pattern}')
    cov.report(file=open(f'/home/soslab/pyct-coverage/coverage_ray/transformers/ct_log/{time_}_chatgpt.txt','w'),ignore_errors=True)
    



# 設定你的 API 金鑰


def ask_chatgpt(question):
    openai.api_key = 'apikey'
    
    response = openai.Completion.create(
        engine="davinci-002",
        prompt=question,
        max_tokens=50
    )
    answer = response.choices[0].text.strip()
    return answer

def ask_anthropic():
    model_name = "claude-2"
    anthropicKey='apikey'
    anthropic_ = anthropic.Anthropic(api_key=anthropicKey,)
    completion = anthropic_.completions.create(
                    model=model_name,
                    prompt=f"how are you?",
                    max_tokens_to_sample=50
                )
    time.sleep(10)    
    return completion.completion





if __name__ == '__main__':  
    # if os.path.exists('/home/soslab/pyct-coverage/coverage_ray/transformers/can_fork_pyct_func.json'):
    #     os.remove('/home/soslab/pyct-coverage/coverage_ray/transformers/can_fork_pyct_func.json')
    # if os.path.exists('/home/soslab/pyct-coverage/coverage_ray/transformers/.coverage'):
    #     os.remove('/home/soslab/pyct-coverage/coverage_ray/transformers/.coverage')

    # if os.path.exists('/home/soslab/pyct-coverage/coverage_ray/transformers/wrapped_fun.json'):
    #     os.remove('/home/soslab/pyct-coverage/coverage_ray/transformers/wrapped_fun.json')
    logging.basicConfig(level=logging.INFO)
    
    import pandas
    # chatGPT_test()
    # unit_test("test_*.py",numpydoc.__file__.replace("__init__.py",""))
    # openai.api_key = 'sk-proj-LOBWfBFPRIhtR9JRqHRTT3BlbkFJik8nzcW87Op9jbuAxmtI'
    unit_pytest('pandas',pandas.__file__.replace("__init__.py",""))
    # program_test()
    
    # answer = ask_anthropic()
    