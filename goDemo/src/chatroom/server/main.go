package main

import (
	"chatroom/common/message"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"io"
	"net"
)

// 封装读取 message，序列化的方法，避免重复调用问题的发生
func readPkg(conn net.Conn) (mes message.Message, err error) {
	buf := make([]byte, 8096)
	// conn.Read()，只有 conn 在没有被关闭的情况下，才会阻塞
	// 如果客户端关闭 conn，则不会阻塞，否则服务端会一直报 error

	// 读客户端发的消息
	// err 在返回参数已经定义，因此不需要使用 := 这样的方式接受 err
	_, err = conn.Read(buf[:4])
	if err != nil {
		//err = errors.New("read pkg header error.")
		return
	}

	// 根据 buf[:4] 转成一个 uint32 类型
	pkgLen := binary.BigEndian.Uint32(buf[:4])
	// 根据 pkgLen 读取消息内容
	// 从套接字内的 buf 流中，读取 pkgLen 个长度的内容
	n, err1 := conn.Read(buf[:pkgLen])
	if n != int(pkgLen) || err1 != nil {
		//fmt.Println("conn.Read(buf[:pkgLen]) is err = ", err1)
		//err = errors.New("read pkg body error.")
		return
	}
	//字符串反序列化
	err = json.Unmarshal(buf[:pkgLen], &mes)
	if err != nil {
		fmt.Println("json.Unmarshal(buf[:pkgLen], &mes) err = ", err)
	}
	return

}

func process(conn net.Conn) {
	defer conn.Close()
	for {
		msg, err := readPkg(conn)
		if err != nil {
			if err == io.EOF {
				fmt.Println("客户端退出，服务器也退出。。。")
				return
			} else {
				fmt.Println("readPkg() err = ", err)
				return
			}
		}
		fmt.Println("msg = ", msg)
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
