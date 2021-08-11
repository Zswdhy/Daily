# 创建一个Hello类，拥有属性say_hello ----二的起源
class Hello():
    def say_hello(self, name='world'):
        print('Hello, %s.' % name)


# Hello().say_hello('China')


class SayMetaClass(type):
    # 传入三大永恒命题：类名称、父类、属性
    def __new__(cls, name, bases, attrs):
        # 创造“天赋”
        attrs['say_' + name] = lambda self, value, saying=name: print(saying + ',' + value + '!')
        # 传承三大永恒命题：类名称、父类、属性
        return type.__new__(cls, name, bases, attrs)


# 一生二：创建类
class Hello(object, metaclass=SayMetaClass):
    pass


# 二生三：创建实列
Hello().say_Hello('中国')
