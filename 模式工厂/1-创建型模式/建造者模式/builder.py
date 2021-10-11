"""
    创建一个由多个部分构成的对象，并且构成需要一步接一步的完，只有各个部门都创建好之后，这个对象才算是完整的创建完成。
    将一个复杂对象的构建过程与其表现分离

    构建者模式与工厂模式的区别：
        意图不同：
            工厂模式关注产品的整体，无需关注产品的各部分的创建过程 ------> 粗线条应用
            构建者模式关注产品从无到有的各个细节创建过程【关注产品的构建过程】 ------> 细线条应用

        产品复杂度：
            工厂模式创建的产品相对单一，对象粒度相对比较粗
            建造者模式创建的是一个符合产品，由各个部分复合而成，部件不同产品对象不同，对象粒度相对较细
    使用场景：
        相同方法，不用执行顺序，产生不同效果
"""
from enum import Enum
import time

# pizza 制作过程 空格切分，使用 枚举名称.field 调用
PizzaProgress = Enum('PizzaProgress', 'queued preparation baking ready')
# pizza 面团
PizzaDough = Enum('PizzaDough', 'thin thick')
# 添加酱汁
PizzaSauce = Enum('PizzaSauce', 'tomato creme_fraiche')
PizzaTopping = Enum('PizzaTopping', 'mozzarella double_mozzarella bacon ham mushrooms red_onion oregano')
STEP_DELAY = 3  # 考虑到这是示例，单位为秒


class Pizza:
    def __init__(self, name):
        self.name = name
        self.dough = None
        self.sauce = None
        self.topping = []

    def __str__(self):
        return self.name

    def prepare_dough(self, dough):
        self.dough = dough
        print('preparing the {} dough of your {}...'.format(self.dough.name, self))
        time.sleep(STEP_DELAY)
        print('done with the {} dough'.format(self.dough.name))


class MargaritaBuilder:
    def __init__(self):
        self.pizza = Pizza('margarita')
        self.progress = PizzaProgress.queued
        self.baking_time = 5  # 考虑是示例，单位为秒

    def prepare_dough(self):
        self.progress = PizzaProgress.preparation
        self.pizza.prepare_dough(PizzaDough.thin)

    def add_sauce(self):
        print('adding the tomato sauce to your margarita...')
        self.pizza.sauce = PizzaSauce.tomato
        time.sleep(STEP_DELAY)
        print('done with the tomato sauce')

    def add_topping(self):
        print('adding the topping (double mozzarella, oregano) to your margarita')
        self.pizza.topping.append([i for i in (PizzaTopping.double_mozzarella, PizzaTopping.oregano)])
        time.sleep(STEP_DELAY)
        print('done with the topping (double mozzarrella, oregano)')

    def bake(self):
        self.progress = PizzaProgress.baking
        print('baking your margarita for {} seconds'.format(self.baking_time))
        time.sleep(self.baking_time)
        self.progress = PizzaProgress.ready
        print('your margarita is ready')


class CreamyBaconBuilder:
    def __init__(self):
        self.pizza = Pizza('creamy bacon')
        self.progress = PizzaProgress.queued
        self.baking_time = 7  # 考虑是示例，单位为秒

    def prepare_dough(self):
        self.progress = PizzaProgress.preparation
        self.pizza.prepare_dough(PizzaDough.thick)

    def add_sauce(self):
        print('adding the crème fraîche sauce to your creamy bacon')

        self.pizza.sauce = PizzaSauce.creme_fraiche
        time.sleep(STEP_DELAY)
        print('done with the crème fraîche sauce')

    def add_topping(self):
        print('adding the topping (mozzarella, bacon, ham, mushrooms, red onion,oregano) to your creamy bacon')
        self.pizza.topping.append([t for t in
                                   (PizzaTopping.mozzarella, PizzaTopping.bacon,
                                    PizzaTopping.ham, PizzaTopping.mushrooms,
                                    PizzaTopping.red_onion, PizzaTopping.oregano)])
        time.sleep(STEP_DELAY)
        print('done with the topping (mozzarella, bacon, ham, mushrooms, red onion, oregano)')

    def bake(self):
        self.progress = PizzaProgress.baking
        print('baking your creamy bacon for {} seconds'.format(self.baking_time))
        time.sleep(self.baking_time)
        self.progress = PizzaProgress.ready
        print('your creamy bacon is ready')


class Waiter:

    def __init__(self):
        self.builder = None

    def construct_pizza(self, builder):
        self.builder = builder
        [step() for step in (builder.prepare_dough, builder.add_sauce, builder.add_topping, builder.bake)]

    @property
    def pizza(self):
        return self.builder.pizza


def validate_style(builders):
    try:
        pizza_style = input('What pizza would you like, [m]argarita or [c]reamy bacon?')
        builder = builders[pizza_style]()
        valid_input = True

    except KeyError as err:
        print('Sorry, only margarita (key m) and creamy bacon (key c) are available')
        return (False, None)
    return (True, builder)


def main():
    builders = dict(m=MargaritaBuilder, c=CreamyBaconBuilder)

    valid_input = False
    while not valid_input:
        valid_input, builder = validate_style(builders)
    print()
    waiter = Waiter()
    waiter.construct_pizza(builder)

    pizza = waiter.pizza
    print()
    print('Enjoy your {}!'.format(pizza))


if __name__ == '__main__':
    main()
