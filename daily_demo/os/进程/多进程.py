# 进程模块
import multiprocessing
import time


class Process(multiprocessing.Process):
    def run(self):
        start = time.time()
        sum = 0
        for n in range(100000000):
            sum += n
        print('cur sum', sum)
        print("data:{}".format(time.time() - start))


if __name__ == '__main__':  # windows在调用进程的时候,必须加这句话,否则会报错
    li = []
    for i in range(2):
        li.append(Process())

    for p in li:
        print('cur process name', p.name)
        p.start()  # 直接执行 run 方法

    for i in li:
        i.join(timeout=None)

    print("ending...")
