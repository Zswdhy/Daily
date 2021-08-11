import random
import time
from multiprocessing import Pipe, Process


def worker(pipe):
    time.sleep(random.random())
    for i in range(10):
        print("worker send {}".format(pipe.send(i)))  # Pipe 的 send 是没有返回值的


def Boss(pipe):
    while True:
        print("Boss recv {}".format(pipe.recv()))


if __name__ == '__main__':
    pipe = Pipe()  # 进程之间的通信   Pipe (类似于 socket )

    print('pipe', pipe)

    p1 = Process(target=worker, args=(pipe[0],))
    p2 = Process(target=Boss, args=(pipe[1],))
    p1.start()
    p2.start()
