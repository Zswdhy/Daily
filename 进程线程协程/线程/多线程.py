import threading  # 线程模块
import time


# 创建线程
def onepiece1(n):
    print("路飞正在使用橡胶火箭炮%s,攻击力%s" % (time.ctime(), n))
    time.sleep(3)
    print("路飞结束该技能%s" % time.ctime())


def onepiece2(n):
    print("艾尼路正在出雷神万击%s你,攻击力%s" % (time.ctime(), n))
    time.sleep(5)
    print("艾尼路结束该技能%s" % time.ctime())


if __name__ == '__main__':
    thread_1 = threading.Thread(target=onepiece1, args=(10,))  # 创建子线程
    thread_2 = threading.Thread(target=onepiece2, args=(9,))

    thread_1.start()
    thread_2.start()
    # thread_1.join()
    thread_2.join()  # 等待线程终止

    print("ending Fighting")
