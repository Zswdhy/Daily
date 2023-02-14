import grpc

from gRPC.settings import hello_pb2, hello_pb2_grpc


def run():
    """
    模拟请求服务方法信息

    :return:
    """
    conn = grpc.insecure_channel('localhost:50052')
    client = hello_pb2_grpc.GrpcServiceStub(channel=conn)
    skill = hello_pb2.Skill(name="engineer")
    print("skill", skill)
    request = hello_pb2.HelloRequest(data="xiao gang", skill=skill)
    try:
        respnse = client.hello(request)
        print("received", str(respnse))
    except Exception as e:
        print("eeee", str(e))


if __name__ == '__main__':
    run()
