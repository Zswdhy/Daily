# 进程之间的通信   Queue
from multiprocessing import Queue, Process
import os, time, random


def write(q):
    print("process to write{}".format(os.getpid()))
    for value in ["A", "B", "C"]:
        print("Put {} to queue...".format(value))
        q.put(value)
        time.sleep(random.random())


def read(q):
    print("process to read{}".format(os.getpid()))
    while True:
        value = q.get(True)
        print("Get {} from queue".format(value))


if __name__ == '__main__':
    q = Queue()
    pw = Process(target=write, args=(q,))  # target 依旧是进程回调函数，使用 args 将队列传递过来
    pr = Process(target=read, args=(q,))
    pw.start()
    pr.start()

    pw.join()
    pr.terminate()  # 强行终止进程(因为这个子进程定义了一个死循环)
