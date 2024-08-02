# 一定要在最一開始import此模組，後續取得自動import的模組清單才不會錯
import sys

import unittest
import sys
import logging
# import tensorflow as tf
import os
import coverage

if __name__ == '__main__':    
    # sys.path.insert(1, "/home/jack/coverage/PyCT/libct")
    # os.remove('.coverage')
    
    # bool
    # 232570 --> 232568
    # pattern = "test_tokenization_utils.py" # tests/tokenization/test_tokenization_utils.py
    
    # str + int
    # 237995 --> 237995
    pattern = "test_audio_utils.py" # tests/utils/test_audio_utils.py
    

    os.environ['run_pyct_in_unittest'] = 'False'
    cov = coverage.Coverage()
    cov.start() # Start measuring coverage
    
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='.', pattern=pattern)
    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(suite)
        
    cov.stop() # Stop measuring coverage
    cov.save() # Save the coverage data to disk
    cov.report(file=open(f'coverage_report_manual/{pattern}_unittest.txt', 'w'))
    

