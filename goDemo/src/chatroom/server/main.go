package main

import (
	"fmt"
	"net"
)

func process(conn net.Conn) {
	defer conn.Close()

	// 读客户端发的消息
	for {
		buf := make([]byte, 8096)
		n, err := conn.Read(buf[:4])
		if n != 4 || err != nil {
			fmt.Println("conn.read err = ", err)
			return
		}
		fmt.Println("读取到的 buf = ", buf[:4])
	}
}

func main() {
	fmt.Println("服务器在8889端口监听。。。")
	listen, err := net.Listen("tcp", "127.0.0.1:8889")
	defer listen.Close()
	if err != nil {
		fmt.Println("net.listen err = ", err)
		return
	}
	for {
		fmt.Println("等待客户端来链接服务器。。。")
		coon, err := listen.Accept()
		if err != nil {
			fmt.Println("listen.Accept() err = ", err)
		}
		// 链接成功，启动协程和客户端保持通讯
		go process(coon)
	}
}
