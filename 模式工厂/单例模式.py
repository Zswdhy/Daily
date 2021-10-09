import threading


class Car:
    INSTANCE = None
    isCreate = True

    def __new__(cls, *args, **kwargs):
        """当 INSTANCE 不存在的时候，就是第一次调用此类 __new__ 方法.因此创建实例对象."""
        if not Car.INSTANCE:
            Car.INSTANCE = super().__new__(cls)
        """当第二次进来的时候，INSTANCE 存在，因此直接返回返回 Car 的实例对象."""
        print(Car.INSTANCE)
        return Car.INSTANCE

    def __init__(self, brand, color, length):
        """
        第一次进行的时候，进行初始化操作.之后的操作进行不进行初始化操作
        :param brand:
        :param color:
        :param length:
        """

        if Car.isCreate:
            self.brand = brand
            self.color = color
            self.length = length
            Car.isCreate = False

    @property
    def car_info(self):
        return {"brand": self.brand, "color": self.color, "length": self.length}


if __name__ == '__main__':
    car1 = Car("五菱宏光", "black", 5.6)
    car2 = Car("长安", "white", 5.5)


    def task(arg):
        obj = Car("五菱宏光", "black", 5.6)
        print(obj)


    for i in range(30):
        t = threading.Thread(target=task, args=[i, ])
        t.start()
