import json

import xml.etree.ElementTree as etree

"""
    工厂模式：
        抽象多个不同的类，根据入参的数据类型自动调用对象的工厂类方法
        类似于 map 映射
    抽象工厂：
        进行功能的解耦，例如造小汽车，一个部件一个方法
    最好采用静态方法，可以直接使用类名调用
"""


class JSONConnector:

    def __init__(self, filepath):
        self.data = dict()
        with open(filepath, mode='r', encoding='utf-8') as f:
            self.data = json.load(f)

    @property
    def parsed_data(self):
        return self.data


class XMLConnector:

    def __init__(self, filepath):
        self.tree = etree.parse(filepath)

    @property
    def parsed_data(self):
        return self.tree


def connection_factory(filepath):
    if filepath.endswith('json'):
        connector = JSONConnector
    elif filepath.endswith('xml'):
        connector = XMLConnector
    else:
        raise ValueError(f'Cannot connect to {filepath}')
    return connector(filepath)


def connect_to(filepath):
    factory = None
    try:
        factory = connection_factory(filepath)
    except ValueError as ve:
        print(f"ValueError:{ve}")
    return factory


if __name__ == '__main__':
    test_factory = connect_to("person.txt")
    print(test_factory, "\n")

    xml_factory = connect_to('person.xml')
    xml_data = xml_factory.parsed_data
    liars = xml_data.findall(".//{}[{}='{}']".format('person', 'lastName', 'Liar'))
    print('found: {} persons'.format(len(liars)))
    for liar in liars:
        print('first name: {}'.format(liar.find('firstName').text))
        print('last name: {}'.format(liar.find('lastName').text))
        [print('phone number ({})'.format(p.attrib['type']), p.text) for p in liar.find('phoneNumbers')]
    print()

    json_factory = connect_to('person.json')
    json_data = json_factory.parsed_data
    print('found: {} donuts'.format(len(json_data)))
