# gRPC

## 定义

[gRPC](http://www.oschina.net/p/grpc-framework)  是一个高性能、开源和通用的 RPC 框架，面向移动和 HTTP/2 设计。目前提供 C、Java 和 Go 语言版本，分别是：grpc, grpc-java, grpc-go. 其中 C 版本支持 C, C++, Node.js, Python, Ruby, Objective-C, PHP 和 C# 支持.

gRPC 基于 HTTP/2 标准设计，带来诸如双向流、流控、头部压缩、单 TCP 连接上的多复用请求等特。这些特性使得其在移动设备上表现更好，更省电和节省空间占用。



## 使用场景

* **微服务** - gRPC设计为低延迟和高吞吐量通信。gRPC非常适用于效率至关重要的轻型微服务。
* **点对点实时通信** - gRPC对双向流媒体提供出色的支持。gRPC服务可以实时推送消息而无需轮询。
* **多语言混合开发环境** - gRPC工具支持所有流行的开发语言，使gRPC成为多语言开发环境的理想选择。
* **网络受限环境** - 使用Protobuf（一种轻量级消息格式）序列化gRPC消息。gRPC消息始终小于等效的JSON消息。


# 案例实践

## 1、安装依赖
```python
pip install grpcio
pip install grpcio-tools
```

## 2、编写 *. proto 文件

## 3、生成 pb 文件
```python
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. first.proto
```

## 4、编写服务端和客户端代码

## 5、启动服务端、客户端代码