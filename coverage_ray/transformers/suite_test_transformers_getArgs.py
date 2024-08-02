# 一定要在最一開始import此模組，後續取得自動import的模組清單才不會錯
import sys
sys.path.insert(0, '/home/jack/mylib')
import arg_wrapper.arg_wrapper as arg_wrapper

import unittest
import sys
import logging
# import tensorflow as tf
import os
import coverage

if __name__ == '__main__':    
    sys.path.insert(1, '/home/jack/coverage/transformers/src')
    # sys.path.insert(1, "/home/jack/coverage/PyCT/libct")
    
    # logging.basicConfig(level=logging.CRITICAL)
    # tf.get_logger().setLevel(tf._logging.FATAL)
    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    # tf.autograph.set_verbosity(5)

    loader = unittest.TestLoader()    
    suite = loader.discover(start_dir='.', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(suite)
    
