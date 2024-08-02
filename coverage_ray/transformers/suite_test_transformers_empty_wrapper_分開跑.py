# 一定要在最一開始import此模組，後續取得自動import的模組清單才不會錯
import sys
sys.path.insert(0, '/home/jack/mylib')
import arg_wrapper.arg_wrapper as arg_wrapper

import unittest
import sys
import logging
from pathlib import Path
import os
import multiprocessing
import coverage
import traceback

# 配置日志
script_file = os.path.basename(__file__)
log_file = f"{os.path.splitext(script_file)[0]}.log"
log_path = os.path.join("log", log_file)
logging.basicConfig(filename=log_path, level=logging.INFO, filemode="w")

if __name__ == '__main__':    
    sys.path.insert(1, '/home/jack/coverage/transformers/src')
    # sys.path.insert(1, "/home/jack/coverage/PyCT/libct")
    
    if os.path.exists("last_i.txt"):
        with open('last_i.txt', 'r') as f:
            max_i = int(f.read().splitlines()[0])
    else:
        max_i = -1
    
    for i, path in enumerate(Path('./tests').rglob('test_*.py')):
        if i <= max_i:
            continue
        
        print("@" * 60)
        logging.info(f"{'@' * 60}")
        logging.info(f"{i:05d} {path}")

        def run_unit_tests(path):
            loader = unittest.TestLoader()
            suite = loader.discover(start_dir='.', pattern=path)
            runner = unittest.TextTestRunner(verbosity=1)
            
            cov = coverage.Coverage()
            cov.load()
            cov.start()
            runner.run(suite)
            cov.stop()
            cov.save()
        
        process = multiprocessing.Process(target=run_unit_tests, args=(path.name, ))
        process.start()
        process.join()
        
        try:
            cov = coverage.Coverage()
            cov.load()
            cov.report(file=open(f'./coverage_report/coverage_report_tests_empty_wrapper{i}.txt', 'w'))
        except Exception as e:
            traceback.print_exc()
        
             
        with open('last_i.txt', 'w') as f:
            f.write(f"{i}\n")

    
    # 关闭日志记录器
    logging.shutdown()
    
