class Plane:
    def __init__(self, name):
        self.name = name

    def move(self):
        pass


class Hero(Plane):
    def __init__(self, name):
        super(Hero, self).__init__(name)

    def move(self):
        print(self.name, "起飞了，准备开火")


class SmallEnemy(Plane):
    def __init__(self, name):
        super(SmallEnemy, self).__init__(name)

    def move(self):
        print(self.name, "小敌机，准备去碰瓷")


class MiddleEnemy(Plane):
    def __init__(self, name):
        super(MiddleEnemy, self).__init__(name)

    def move(self):
        print(self.name, "中等飞机，也准备去碰英雄飞机")


class BigEnemy(Plane):
    def __init__(self, name):
        super(BigEnemy, self).__init__(name)

    def move(self):
        print(self.name, "大飞机，去碰瓷了")


class PlaneFactory:
    @staticmethod
    def createPlane(planeName):
        if planeName == "英雄飞机":
            return Hero("英雄飞机")
        elif planeName == "小敌机":
            return SmallEnemy("小敌机")
        elif planeName == "中等飞机":
            return MiddleEnemy("中等飞机")
        elif planeName == "大飞机":
            return BigEnemy("大飞机")


# with open("plane.txt", "r", encoding="utf-8") as file:
#     PlaneFactory.createPlane(file.read()).move()

PlaneFactory.createPlane("英雄飞机").move()
