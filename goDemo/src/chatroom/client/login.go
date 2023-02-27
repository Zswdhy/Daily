package main

import (
	"chatroom/common/message"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"net"
	"time"
)

func login(userId int, passWord string) (err error) {

	// 1、链接服务器
	conn, err := net.Dial("tcp", "localhost:8889")
	if err != nil {
		fmt.Println("net.Dial err = ", err)
		return
	}

	defer conn.Close()

	// 2、发送消息
	var msg message.Message
	msg.Type = message.LoginMesType
	// 3、创建LoginMes 结构体
	var loginMes message.LoginMes
	loginMes.UserId = userId
	loginMes.UserPwd = passWord
	// 4、将 loginMes 序列化

	data, err := json.Marshal(loginMes)
	if err != nil {
		fmt.Println("json.Marshal err =", err)
	}
	// data 是 [] 切片类型，需要转换成字符串
	msg.Data = string(data)

	// 将整体的 Mes 序列化
	data, err = json.Marshal(msg)
	if err != nil {
		fmt.Println("json.Marshal err =", err)
	}

	// 先把 data 的成都发送给服务器，进行字符串判断
	var pkgLen uint32
	pkgLen = uint32(len(data))
	var buf [4]byte
	// 将 int 类型的数据转换成 byte[]
	binary.BigEndian.PutUint32(buf[:4], pkgLen)

	n, err := conn.Write(buf[:4])
	if n != 4 || err != nil {
		fmt.Println("conn.write err = ", err)
		return
	}
	fmt.Printf("客户端发送消息长度成功... len = %d , data = %s ", len(data), string(data))

	// 发送消息体本身
	_, err = conn.Write(data)
	if err != nil {
		fmt.Println("conn.write err = ", err)
		return
	}
	time.Sleep(20 * time.Second)
	fmt.Println("客户端正在取消链接。。。,20秒链接")
	return
}
