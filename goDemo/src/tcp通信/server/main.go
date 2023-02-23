package main

import (
	"fmt"
	"net"
)

func process(conn net.Conn) {
	defer conn.Close()

	for {

		buf := make([]byte, 1024)

		fmt.Println("服务器正在的呢过在客户端 %s  发送消息\n", conn.RemoteAddr().String())
		n, err := conn.Read(buf)
		if err != nil {
			fmt.Println("客户端退出  err = ", err)
			return
		}
		fmt.Println(string(buf[:n]))
	}
}

func main() {
	fmt.Println("服务器开始监听...")
	listen, err := net.Listen("tcp", "localhost:8888")
	if err != nil {
		fmt.Println("net.Listen() err = ", err)
		return
	}
	defer listen.Close()

	for {
		fmt.Println("等待客户端链接...")
		conn, err := listen.Accept()
		if err != nil {
			fmt.Println("Accept err = ", err)
			return
		} else {
			fmt.Printf("Accept() success conn = %v 客户端 ip = %v\n", conn, conn.RemoteAddr().String())
		}
		go process(conn)
	}
}
