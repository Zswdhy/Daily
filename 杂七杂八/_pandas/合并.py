import pandas as pd
import numpy as np


def merge_basic():
    df1 = pd.DataFrame({'alpha': ['A', 'B', 'B', 'C', 'D', 'E'], 'beta': ['a', 'a', 'b', 'c', 'c', 'e'],
                        'feature1': [1, 1, 2, 3, 3, 1], 'feature2': ['low', 'medium', 'medium', 'high', 'low', 'high']})

    df2 = pd.DataFrame(
        {'alpha': ['A', 'A', 'B', 'F'], 'beta': ['d', 'd', 'b', 'f'], 'pazham': ['apple', 'orange', 'pine', 'pear'],
         'kilo': ['high', 'low', 'high', 'medium'], 'price': np.array([5, 6, 5, 7])})

    # how:['left','right','inner','outer']
    # on:可以是单列，也可以是多列【多列使用 list 】
    df8 = pd.merge(df1, df2, how='right', on=['alpha', 'beta'])

    return df8


def merge_plus():
    df1 = pd.DataFrame({'alpha': ['A', 'B', 'B', 'C', 'D', 'E'], 'beta': ['a', 'a', 'b', 'c', 'c', 'e'],
                        'feature1': [1, 1, 2, 3, 3, 1], 'feature2': ['low', 'medium', 'medium', 'high', 'low', 'high']})

    df2 = pd.DataFrame({'alpha': ['A', 'A', 'B', 'F'], 'pazham': ['apple', 'orange', 'pine', 'pear'],
                        'kilo': ['high', 'low', 'high', 'medium'], 'price': np.array([5, 6, 5, 7])},
                       index=['d', 'd', 'b', 'f'])

    # 基于 df1 的 beta 列和 df2 的 index 连接
    """
        left_on/right_on:和正常的 on 参数效果一样
        left_index/right_index:布尔类型 使用对应的 index  进行匹配，使用不一样的字段名称的匹配
    """
    df9 = pd.merge(df1, df2, how='inner', left_on='beta', right_index=True)
    return df9


def inner_basic():
    caller = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3', 'K4', 'K5'], 'A': ['A0', 'A1', 'A2', 'A3', 'A4', 'A5']})
    other = pd.DataFrame({'key': ['K0', 'K1', 'K2'], 'B': ['B0', 'B1', 'B2']})

    # 基于索引的 inner
    # caller.set_index('key').join(other.set_index('key'),how='inner')

    # lsuffix和rsuffix设置连接的后缀名
    return caller.join(other, lsuffix='_caller', rsuffix='_other', how='inner')


def concat_basic():
    df1 = pd.Series([1.1, 2.2, 3.3], index=['i1', 'i2', 'i3'])
    df2 = pd.Series([4.4, 5.5, 6.6], index=['i2', 'i3', 'i4'])

    # 行拼接
    # axis=0 默认行拼接，axis=1 默认是列拼接
    return pd.concat([df1, df2], axis=0)


if __name__ == '__main__':
    # print(merge_basic())
    # print(merge_plus())
    # print(inner_basic())
    print(concat_basic())
