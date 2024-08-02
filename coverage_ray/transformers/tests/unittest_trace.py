import unittest
from .. import trace_test as tt 
class trace_testcase(unittest.TestCase):

    def test_trace(self):
        tt.branch_test(5,a=0)
        
if __name__=='__main__':
    unittest.main()
