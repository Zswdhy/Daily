import time


def calculate_time(func):
    print("e")

    def start_calculate(*args, **kwargs):
        print("f")
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} spend:", time.time() - start_time)
        return result

    print("g")
    return start_calculate


@calculate_time
def fibonacci(n):
    print("a")
    if n >= 1:
        print("b")
        if n in [1, 2]:
            print("c")
            return 1
        else:
            print("d")
            return fibonacci(n - 1) + fibonacci(n - 2)
    return False


if __name__ == '__main__':
    cur_time = time.time()
    print("结果", fibonacci(3))
    print(f"spend time: {time.time() - cur_time}")
