import sys
import logging
import traceCall as tc
import os
import coverage
import time
import unittest



class testClass():
    def t(self,a):
        branch_test_kwarg(3,kw=0)
        if a==0:
            return True
        else:
            return False
        
def branch_test_nothing():
    a()
    b()

def a():
    c()

def b():
    pass

def c():
    pass

def branch_test(b,a):
        if a==0:
            return True
        else:
            return False
        
def branch_test_matrix(a):
        if a[0]==0:
            return True
        else:
            return False

def branch_test_dict(a):
        if a['k']==0:
            return True
        else:
            return False
        
def branch_test_kwarg(a,**kwargs):
        if kwargs['kw']==0:
            return True
        else:
            return False
        
def branch_test_arg(*args):
        if len(args)>2:
            return True
        else:
            return False
        
def branch_test_type(a,*args,b=10,**kwargs):
    if kwargs['c']==0:
        return True
    else:
        return False
        
def branch_test_everything():
    c=testClass()
    d=testClass()
    c.t(0)
    branch_test(5,a=0)
    branch_test_matrix([3,2])
    branch_test_dict({'k':0})
    branch_test_arg(3,2,5,6)
    branch_test_kwarg(3,kw=0)
    branch_test_type(3,*(2,3),b=10,c=10,**{'d':5})

class trace_testcase(unittest.TestCase):

    def test_trace(self):
        branch_test(5,a=0)

# def deathlock_test_1(a):
#     if a==0:
#         deathlock_test_2(0)
#         return True
#     else:
#         return False
    
# def deathlock_test_2(a):
#     if a==0:
#         deathlock_test_1(0)
#         return 1
#     else:
#         return False
# 设置跟踪函数
# if os.path.exists('can_fork_pyct_func.json'):
#         os.remove('can_fork_pyct_func.json')

if __name__=='__main__':
     
    FORMAT = '%(funcName)s %(lineno)s: %(message)s'
    logging.basicConfig(level=logging.INFO,format=FORMAT)
    time_result = time.localtime(time.time())
    time_=f'{time_result.tm_mon}_{time_result.tm_mday}'
    if os.path.exists('can_fork_pyct_func.json'):
        os.remove('can_fork_pyct_func.json')
        
    if os.path.exists('wrapped_fun.json'):
        os.remove('wrapped_fun.json')

    # cov = coverage.Coverage()
    # cov.start() # Start measuring coverage
    sys.setprofile(tc.trace_calls)

    # 调用函数
    # print(f"call function result:{branch_test(5,a=0)}")
    # print(f"call function result:{branch_test_matrix([3,2])}")
    # print(f"call function result:{branch_test_dict({'k':0})}")
    # print(f"call function result:{branch_test_arg(3,2,5,6)}")
    # print(f"call function result:{branch_test_kwarg(3,kw=0)}")
    # print(f"call function result:{branch_test_type(3,*(2,3),b=10,c=10,**{'d':5})}")
    # print(f"call function result:{branch_test_nothing()}")

    # branch_test(5,a=0)
    # branch_test_matrix([3,2])
    # branch_test_dict({'k':0})
    # branch_test_arg(3,2,5,6)
    # branch_test_kwarg(3,kw=0)
    # branch_test_type(3,*(2,3),b=10,c=10,**{'d':5})
    # branch_test_nothing()
    branch_test_everything()


    # 取消跟踪函数
    sys.setprofile(None)
    # cov.stop() # Stop measuring coverage
    # cov.save() # Save the coverage data to disk
    # cov.report(file=open(f'ct_log/{time_}_traceTest.txt', 'w'),)
    # cov.html_report(directory=f'ct_log/{time}/cov_report',title=f'traceTest_unittest.txt')