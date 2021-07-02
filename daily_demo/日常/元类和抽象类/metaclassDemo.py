class Mymeta(type):

    def __init__(self, name, base, dic):
        super().__init__(name, base, dic)

        print('Mymeta,init')
        print('Mymeta name', self.__name__)
        print('Mymeta dic', self.__dir__)
        print('Mymeta yaml tag', self.yaml_tag)

    def __new__(cls, *args, **kwargs):
        print('Mymeta new')
        print('Mymeta new', cls.__name__)
        return type.__new__(cls, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        print('===>Mymeta.__call__')
        obj = cls.__new__(cls)
        cls.__init__(cls, *args, **kwargs)

        return obj


class Foo(metaclass=Mymeta):
    yaml_tag = '!Foo'

    def __init__(self, name):
        print('Foo.__init__')
        self.name = name

    def __new__(cls, *args, **kwargs):
        print('Foo.__new__')
        return object.__new__(cls)


foo = Foo('haiyul')
