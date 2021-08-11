import asyncio
import websockets


# 检测客户端权限，用户名密码通过才能退出循环
async def check_permit(websocket):
    while True:
        recv_str = await websocket.recv()  # 接受信息
        cred_dict = recv_str.split(":")
        if cred_dict[0] == "admin" and cred_dict[1] == "123456":
            response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
            await websocket.send(response_str)
            print('client connect success\n')
            return True
        else:
            response_str = "sorry, the username or password is wrong, please submit again"
            await websocket.send(response_str)


# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def recv_msg(websocket):
    while True:
        recv_text = await websocket.recv()
        print('wait  client send message ...\n')
        print(f"your get context: {recv_text}")
        _text = input("please enter your context: ")
        await websocket.send(_text)


# 服务器端主逻辑
# websocket和path是该函数被回调时自动传过来的，不需要自己传
async def main_logic(websocket, path):
    print('wait client ...\n')

    await check_permit(websocket)

    await recv_msg(websocket)


# 创建 websocket server
start_server = websockets.serve(main_logic, '192.168.31.136', 5678)

"""
主线程调用asyncio.get_event_loop()时会创建事件循环，
把异步的任务丢给这个循环的run_until_complete()方法
"""
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
