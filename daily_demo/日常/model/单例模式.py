class Car:
    instance = None
    isCreate = False

    def __new__(cls, *args, **kwargs):
        # 懒汉式创建
        if Car.instance == None:
            Car.instance = super(Car, cls).__new__(cls)
        return Car.instance

    # 初始化属性数据
    def __init__(self, brand, color, wheel):
        if Car.isCreate == False:
            self.brand = brand
            self.color = color
            self.wheel = wheel
            Car.isCreate = True

    def show(self):
        print('品牌', self.brand, '颜色', self.color, '轮子', self.wheel)


c1 = Car("大奔", "黑色", 4)
c1.show()
print(id(c1))

c2 = Car("奥迪", "银色", 4)
c2.show()
print(id(c2))
