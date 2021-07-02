# 双层返回，外部函数返回内部函数的方法名
# 在调用外部函数的时候，返回的是内部函数的方法体
# 调用返回的函数，实质调用内部函数
def out(a, b):
    def inner():
        print(a + b)
        print("inner")

    return inner


demo = out(1, 2)
print(demo)
