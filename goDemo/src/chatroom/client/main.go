package main

import (
	"fmt"
	"os"
)

var userId int
var passWord string

func main() {
	fmt.Println("多人在线聊天室...")
	// 接受用户的选择
	var key int
	//判断是否还继续显示菜单
	var loop = true

	for loop {
		fmt.Println("--------------------欢迎登陆多人聊天系统--------------------")
		fmt.Print("					 1、登陆聊天室\n")
		fmt.Print("					 2、注册用户\n")
		fmt.Print("					 3、退出系统\n")
		fmt.Print("					 请选择（1-3）：")
		fmt.Scanf("%d\n", &key)
		switch key {
		case 1:
			fmt.Println("登陆聊天室")
			loop = false
		case 2:
			fmt.Println("注册用户")
			loop = false
		case 3:
			fmt.Println("退出系统")
			os.Exit(0)
		default:
			fmt.Println("你的输入有误，请重新输入")
		}
	}

	// 根据用户的输入，显示其他的提示信息
	if key == 1 {
		// 用户登陆
		fmt.Println("请输入用户的账号：")
		fmt.Scan(&userId)
		fmt.Println("请输入用户的密码：")
		fmt.Scan(&passWord)
		// 同包下的方法可以直接引用
		err := login(userId, passWord)
		if err != nil {
			fmt.Println("登陆失败：", err)
		} else {
			fmt.Println("登陆成功")
		}
	} else if key == 2 {
		fmt.Println("用户注册逻辑")
	} else if key == 3 {
		fmt.Println("用户退出逻辑")
	}

}
