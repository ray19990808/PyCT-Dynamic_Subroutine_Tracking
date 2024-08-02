import inspect
import sys

class MyClass:
    def method1(self):
        print("Inside method1")
        self.method2()

    def method2(self):
        print("Inside method2")

def trace_calls(frame, event, arg):
    if event == 'call':
        caller_frame = frame.f_back
        caller_name = caller_frame.f_code.co_name
        caller_obj = caller_frame.f_locals.get('self')
        if caller_name != '__init__':
            print(f"{caller_name} called {frame.f_code.co_name} of {caller_obj}")

    return trace_calls

# 创建 MyClass 实例
my_instance = MyClass()

# 设置 trace_calls 作为追踪函数
sys.settrace(trace_calls)

# 调用 method1
my_instance.method1()

# 停止追踪
sys.settrace(None)