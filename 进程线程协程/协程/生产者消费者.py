# 协程
# 生产者生产消息后，直接通过yield跳转到消费者开始执行，待消费者执行完毕后，切换回生产者继续生产，效率极高：
def consumer():
    v = None
    while 1:
        m = yield v
        if not m:
            return
        print("[C]CLine：%s, CProduce:%s" % (m, v))
        v = 'range'


def producter():
    i = 0
    c = consumer()
    c.__next__()
    while i < 5:
        try:
            i += 1
            print(u'[P]producing...%s' % i)
            v = c.send(i)
            print(u'[P]CReturn: %s' % v)
        except StopIteration:
            print('Done!')
            break
    c.close()


if __name__ == '__main__':
    producter()
