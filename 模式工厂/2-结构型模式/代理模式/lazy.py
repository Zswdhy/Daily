class LazyProperty:
    """
    懒汉式加载，只在实际使用的时候才实例化.
    """

    def __init__(self, method):
        self.method = method
        self.method_name = method.__name__

    def __get__(self, instance, owner):
        if not instance:
            return None

        value = self.method(instance)
        """设置实例属性的值.【getattr获取实例对象的属性】"""
        setattr(instance, self.method_name, value)
        return value


class Test:
    def __init__(self):
        self.x = "foo"
        self.y = "bar"
        self._resource = None

    """
        当代码首次加载到这里的时候，就会调用 LazyProperty __init__ func.
        因为 LazyProperty 重写了 __get__ func，非首次调用的时候会执行 __get__ func
        使得 resource() 方法当做了一个变量，因此只实例了一次    
    """
    @LazyProperty
    def resource(self):
        print('initializing self._resource which is: {}'.format(self._resource))
        self._resource = tuple(range(5))
        return self._resource


def main():
    t = Test()
    print(t.x)
    print(t.y)

    print(t.resource)
    print(t.resource)


if __name__ == '__main__':
    main()
