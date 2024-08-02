import unittest
import sys
import logging
# import tensorflow as tf
import os
import coverage


if __name__ == '__main__':    
    sys.path.insert(0, '/home/jack/coverage/PyCT/transformers/src')
    sys.path.insert(1, "/home/jack/coverage/PyCT/libct")
    
    # logging.basicConfig(level=logging.CRITICAL)
    # tf.get_logger().setLevel(tf._logging.FATAL)
    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    # tf.autograph.set_verbosity(5)
    
    # Create a coverage instance
    cov = coverage.Coverage()

    # Start measuring coverage
    cov.start()
    
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='.', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(suite)
        
    # Stop measuring coverage
    cov.stop()

    # Generate a coverage report
    cov.report()


