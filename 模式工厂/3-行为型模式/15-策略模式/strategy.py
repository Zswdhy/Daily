import time

SLOW = 3
LIMIT = 5
WARNING = "too bad,you picked the slow algorithm ：（"


def pairs(seq):
    n = len(seq)
    for i in range(n):
        """当元素和下一次元素（当执行到最后一个位置是，最后一个元素和第一个元素）."""
        yield seq[i], seq[(i + 1) % n]


def all_unique_sort(s):
    """
    sorted 排序.
    :param s:
    :return:
    """
    if len(s) > LIMIT:
        print(WARNING)
        time.sleep(SLOW)
    str_sort = sorted(s)
    for c1, c2 in pairs(str_sort):
        if c1 == c2:
            return False
    return True


def all_unique_set(s):
    """
    set 去重.
    :param s:
    :return:
    """
    if len(s) < LIMIT:
        print(WARNING)
        time.sleep(SLOW)
    return True if len(set(s)) == len(s) else False


def all_unique(s, strategy):
    return strategy(s)


def main():
    while True:
        word = None

        while not word:
            word = input('Insert word (type quit to exit) > ')

            if word == 'quit':
                print('bye')
                return
            strategy_picked = None
            strategies = {'1': all_unique_set, '2': all_unique_sort}
            while strategy_picked not in strategies.keys():
                strategy_picked = input('Choose strategy: [1] Use a set, [2] Sort and pair > ')
            try:
                strategy = strategies[strategy_picked]
                print('allUnique({}): {}'.format(word, all_unique(word, strategy)))
            except KeyError as err:
                print('Incorrect option: {}'.format(strategy_picked))
                print()


if __name__ == '__main__':
    main()
