def demo():
    for i in range(2, 101):
        flag = True
        for j in range(2, i):
            if i % j == 0:
                flag = False
        if flag:
           yield i


print(demo())
for item in demo():
    print(item)


def demo1(num):
    n, a, b = 0, 1, 1
    while n < num:
        a, b = b, a + b
        n += 1
        yield a


