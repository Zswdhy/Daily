package main

import (
	"InformationManagement/model"
	"InformationManagement/server"
	"fmt"
	"strings"
)

type customerView struct {
	key            string //接受用户的输入
	loop           bool   //循环结束的标签
	customerServer *server.CustomerServer
}

// ShowMenu 起始页
func (c *customerView) ShowMenu() string {
	fmt.Println("-----------------------客户信息管理软件----------------------")
	fmt.Println("                       1、添加客户")
	fmt.Println("                       2、修改客户")
	fmt.Println("                       3、删除客户")
	fmt.Println("                       4、客户列表")
	fmt.Println("                       5、退   出")
	fmt.Println("请选择（1-5）")
	fmt.Scan(&c.key)
	return c.key
}

// AddUser 1、新增用户
func (c *customerView) AddUser() {
	fmt.Println("-------------------------添加客户------------------------")
	name := ""
	sex := ""
	age := 0
	phone := ""
	email := ""
	fmt.Print("姓名：")
	fmt.Scan(&name)
	fmt.Print("性别：")
	fmt.Scan(&sex)
	fmt.Print("年龄：")
	fmt.Scan(&age)
	fmt.Print("电话：")
	fmt.Scan(&phone)
	fmt.Print("邮箱：")
	fmt.Scan(&email)
	customer := model.NewCustomerPlus(name, sex, age, phone, email)
	if c.customerServer.Add(*customer) {
		fmt.Println("添加成功")
	} else {
		fmt.Println("添加失败")
	}
}

// Update 2、更新用户
func (c *customerView) Update() {
	fmt.Println("--------------------------修改客户-------------------------")
	fmt.Println("请选择待修改的客户编号（-1退出）:")
	number := 0
	fmt.Scan(&number)
	if number == -1 {
		return
	} else {
		if c.customerServer.UpdateUser(number) {
			fmt.Println("--------------------------修改完成-------------------------")
		} else {
			fmt.Println("--------------------------修改失败-------------------------")
		}
	}
}

// Delete 3、删除用户
func (c *customerView) Delete() {
	fmt.Println("--------------------------删除列表-------------------------")
	fmt.Println("请输入待删除的客户编号（-1退出）")
	number := 0
	fmt.Scan(&number)
	if number == -1 {
		return
	} else {
		fmt.Println("确认是否删除(Y/N):")
		choice := ""
		fmt.Scan(&choice)
		if strings.ToUpper(choice) == "Y" {
			if c.customerServer.DeleteUser(number) {
				fmt.Println("--------------------------删除成功-------------------------")
			} else {
				fmt.Println("--------------------------删除失败-------------------------")
			}
		} else {
			//非Y字符
			return
		}
	}
}

// ClientList 4、列表详情
func (c *customerView) ClientList() {
	fmt.Println("--------------------------客户列表-------------------------")
	fmt.Println("编号\t姓名\t性别\t年龄\t电话\t邮箱")
	for _, c := range c.customerServer.List() {
		//获取单独用户的信息
		fmt.Println(c.GetInfo())
	}
	fmt.Printf("-----------------------客户列表完成-------------------------\n\n")
}

// Quit 5、退出方法体
func (c *customerView) Quit() {
	fmt.Println("确认是否退出(Y/N):")
	for {
		fmt.Scan(&c.key)
		if strings.ToUpper(c.key) == "Y" || strings.ToUpper(c.key) == "N" {
			break
		}
		fmt.Println("你的输入有误，确实是否退出(Y/N)")
	}
	if strings.ToUpper(c.key) == "Y" {
		c.loop = false
		return
	}
}

// MainInterface 入口函数
func (c *customerView) MainInterface() {
	for {
		c.key = c.ShowMenu()
		switch c.key {
		case "1":
			//新增用户
			c.AddUser()
		case "2":
			c.Update()
		case "3":
			//删除
			c.Delete()
		case "4":
			//列表详情
			c.ClientList()
		case "5":
			c.Quit()
		default:
			fmt.Println("错误输入，请输入（1-5）")
		}
		//退出程序
		if !c.loop {
			break
		}
	}
}

func main() {
	customer := customerView{key: "", loop: true, customerServer: server.NewCustomerServer()}
	customer.MainInterface()
}
