import time

def decorator(func):
    def wrapper(me_instance):
        start_time = time.time()
        func(me_instance)
        end_time = time.time()
        print(end_time - start_time)
    return wrapper

class Method(object):

    @decorator
    def func(self):
        time.sleep(0.8)

p1 = Method()
p1.func() # 函数调用