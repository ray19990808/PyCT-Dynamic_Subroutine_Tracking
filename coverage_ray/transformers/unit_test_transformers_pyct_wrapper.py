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
logging.basicConfig(filename=log_path, level=logging.INFO, filemode="a")

if __name__ == '__main__':    
    sys.path.insert(1, '/home/jack/coverage/transformers/src')
    # sys.path.insert(1, "/home/jack/coverage/PyCT/libct")
    os.environ['run_pyct_in_unittest'] = 'True'
    # os.environ['run_pyct_in_unittest'] = 'False'

    # path = Path("test_processor_sam.py") # tests/models/sam/test_processor_sam.py
    # pattern = "test_tokenization_utils.py" # tests/tokenization/test_tokenization_utils.py
    pattern = "test_audio_utils.py" # tests/utils/test_audio_utils.py
    
    print("@" * 60)
    logging.info(f"{'@' * 60}")
    logging.info(f"{pattern}")

    def run_unit_tests(pattern):
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir='.', pattern=pattern)
        runner = unittest.TextTestRunner(verbosity=1)
        
        runner.run(suite)

    
    process = multiprocessing.Process(target=run_unit_tests, args=(pattern, ))
    process.start()
    process.join()


    # 关闭日志记录器
    logging.shutdown()
    
