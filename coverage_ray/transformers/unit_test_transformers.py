# 一定要在最一開始import此模組，後續取得自動import的模組清單才不會錯
import os
import sys
# sys.path.insert(0,os.path.dirname(os.getcwd()))
import unittest


import time
import logging
# import tensorflow as tf

import coverage




import traceCall as tc



def unit_test(pattern,dir):
    
    
    time_result = time.localtime(time.time())
    time_=f'{time_result.tm_mon}_{time_result.tm_mday}'

    cov = coverage.Coverage(auto_data=True)
    cov.start() # Start measuring coverage
    os.chdir(dir)
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=dir, pattern=pattern)
    runner = unittest.TextTestRunner(verbosity=1)
    
    sys.setprofile(tc.trace_calls)
    runner.run(suite)
    sys.setprofile(None)
    
    cov.stop() # Stop measuring coverage
    cov.save() # Save the coverage data to disk
    # cov.html_report(directory=f'ct_log/{time_}/cov_report',title=f'{pattern}')
    cov.report(file=open(f'/home/soslab/pyct-coverage/coverage_ray/transformers/ct_log/{time_}_{pattern}.txt','w'),ignore_errors=True)
    

    return





if __name__ == '__main__':  

    if os.path.exists('/home/soslab/pyct-coverage/coverage_ray/transformers/can_fork_pyct_func.json'):
        os.remove('/home/soslab/pyct-coverage/coverage_ray/transformers/can_fork_pyct_func.json')

    if os.path.exists('/home/soslab/pyct-coverage/coverage_ray/transformers/.coverage'):
        os.remove('/home/soslab/pyct-coverage/coverage_ray/transformers/.coverage')

    if os.path.exists('/home/soslab/pyct-coverage/coverage_ray/transformers/wrapped_fun.json'):
        os.remove('/home/soslab/pyct-coverage/coverage_ray/transformers/wrapped_fun.json')
    logging.basicConfig(level=logging.INFO)
    

    # 看一下.coverage
    # sys.setprofile(tc.trace_calls)
    
    unit_test("trace_test.py",'/home/soslab/pyct-coverage/coverage_ray/transformers')
    # sys.setprofile(None)
    # unit_test("test*.py")

    
    
    

