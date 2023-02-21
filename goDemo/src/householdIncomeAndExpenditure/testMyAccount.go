package main

import "fmt"

//面向过程编程
func test1() {
	//初始金额
	balance := 10000.0
	//每次收支的金额
	money := 0.0
	//每次收支的记录
	note := ""
	//收支的详情，界面文本
	details := "收支\t账户金额\t收支金额\t说明\n"
	//是否有收支行为
	flag := false
	for {
		isQuit := true

		key := ""
		fmt.Println("-----------------------家庭收支记账软件----------------------")
		fmt.Println("                       1、收支明细")
		fmt.Println("                       2、登记收入")
		fmt.Println("                       3、登记支出")
		fmt.Println("                       4、退出软件")
		fmt.Println("请选择（1-4）")
		fmt.Scanln(&key)
		switch key {
		case "1":
			fmt.Println("--------------------当前收支明细记录---------------------")
			if flag {
				fmt.Println(details)
			} else {
				fmt.Println("当前没有收支明细")
			}
		case "2":
			fmt.Println("本次收入金额：")
			fmt.Scan(&money)
			balance += money
			fmt.Println("本次收入说明：")
			fmt.Scan(&note)
			details += fmt.Sprintf("收入\t%v\t%v\t%v\t\n", balance, money, note)
			flag = true
		case "3":
			fmt.Println("本次支出金额：")
			fmt.Scan(&money)
			if money > balance {
				fmt.Println("支出的金额不能大于余额")
				break
			}
			balance -= money
			fmt.Println("本次支出说明：")
			fmt.Scan(&note)
			details += fmt.Sprintf("支出\t%v\t%v\t%v\t\n", balance, money, note)
			flag = true
		case "4":
			fmt.Println("你确定要退出吗？ y/n")
			choice := ""
			for {
				fmt.Scan(&choice)
				if choice == "y" || choice == "n" {
					break
				}
				fmt.Println("你的输入有误，请重新输入 y/n")
			}
			if choice == "y" {
				isQuit = false
				fmt.Println("退出程序中 ...")
			}
			break
		default:
			fmt.Println("错误的选择", key)
		}
		if !isQuit {
			fmt.Println("程序已退出")
			break
		}
	}
}

//面向对象编程
func test2() {

}

func main() {
	test1()
}
