"""
    开放/封闭原则：
        软件实体对功能扩展是开放的
        对修改是封闭的

    适配器模式：
        产品开发出来后，需要用对新的需求
            不要求访问他方接口的源代码
            不违反开放/封闭原则
        解决不同接口之间的兼容问题
        自定义的方法以及调用方式，映射为和之前代码一样的传参形式和调用方式
"""

from external import Synthesizer, Human


class Computer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"the {self.name} computer"

    def execute(self):
        return "execute a program"


class Adapter:
    def __init__(self, obj, adapter_methods):
        self.obj = obj
        self.__dict__.update(adapter_methods)

    def __str__(self):
        return str(self.obj)


if __name__ == '__main__':
    objects = [Computer("Asus"), ]
    """将原本的方法映射为统一的方法进行调用."""
    synth = Synthesizer("moog")
    objects.append(Adapter(synth, dict(execute=synth.play)))
    human = Human("Bob")
    objects.append(Adapter(human, dict(execute=human.speak)))

    for item in objects:
        """ item 默认会调用 __str__ 方法."""
        print("item", type(item))
        print(f"{item} {item.execute()}")
