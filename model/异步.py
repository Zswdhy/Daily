import asyncio


def func1():
    yield 1
    yield from func2()
    yield 2


def func2():
    yield 3
    yield 4


async def func3():
    print(1)
    await asyncio.sleep(2)
    print(2)


async def func4():
    print(3)
    await asyncio.sleep(2)
    print(4)


async def others():
    print("start")
    await asyncio.sleep(2)
    print('end')
    return '返回值'


async def func():
    print("执行协程函数内部代码")
    # 遇到IO操作挂起当前协程（任务），等IO操作完成之后再继续往下执行。当前协程挂起时，事件循环可以去执行其他协程（任务）。
    response = await others()
    print("IO请求结束，结果为：", response)

    response2 = await others()
    print("IO请求结束，结果为：", response2)


if __name__ == '__main__':
    f1 = func1()
    for item in f1:
        print(item)

    print('-' * 100)

    tasks = [
        asyncio.ensure_future(func3()),
        asyncio.ensure_future(func4())
    ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    print('-' * 100)

    asyncio.run(func())
