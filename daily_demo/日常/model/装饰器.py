def wrapper(func):
    print("func", func)
    b = "I am b"

    def inner(a):
        print(a, b)
        print("before")
        ret = func(a)
        print("inner", "after")
        return ret

    return inner


@wrapper
def show_list(b):
    print("show_list")


show_list("I am a!!!")
