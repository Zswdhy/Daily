package utils

import "fmt"

type FamilyAccount struct {
	Balance float64
	//每次收支的金额
	Money float64
	//每次收支的记录
	Note string
	//收支的详情，界面文本
	Details string
	//是否有收支行为
	Flag bool
	//是否退出
	IsQuit bool
}

// ShowMenu 菜单页
func (f *FamilyAccount) ShowMenu() (selectNum string) {
	fmt.Println("-----------------------家庭收支记账软件----------------------")
	fmt.Println("                       1、收支明细")
	fmt.Println("                       2、登记收入")
	fmt.Println("                       3、登记支出")
	fmt.Println("                       4、退出软件")
	fmt.Println("请选择（1-4）")
	fmt.Scan(&selectNum)
	return
}

// AccountDetails 收支明细
func (f *FamilyAccount) AccountDetails() {
	if !f.Flag {
		fmt.Println("还未进行进出账。。。")
	} else {
		fmt.Println(f.Details)
	}
}

// Income 收入
func (f *FamilyAccount) Income() {
	fmt.Println("本次收入金额：")
	fmt.Scan(&f.Money)
	f.Balance += f.Money
	fmt.Println("本次收入说明：")
	fmt.Scan(&f.Note)
	f.Details += fmt.Sprintf("收入\t%v\t%v\t%v\t\n", f.Balance, f.Money, f.Note)
	f.Flag = true
}

// Expenditure 支出
func (f *FamilyAccount) Expenditure() {

	fmt.Println("本次支出金额：")
	fmt.Scan(&f.Money)
	if f.Money > f.Balance {
		fmt.Println("支出的金额不能大于余额")
	} else {
		f.Balance -= f.Money
		fmt.Println("本次支出说明：")
		fmt.Scan(&f.Note)
		f.Details += fmt.Sprintf("支出\t%v\t%v\t%v\t\n", f.Balance, f.Money, f.Note)
		f.Flag = true
	}
}

// Quit 退出程序
func (f *FamilyAccount) Quit() {
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
		f.IsQuit = false
		fmt.Println("退出程序中 ...")
	}
}

// MainInterface 主函数
func (f *FamilyAccount) MainInterface() {
	for {
		if f.IsQuit {
			selectNum := f.ShowMenu()
			switch selectNum {
			case "1":
				f.AccountDetails()
			case "2":
				f.Income()
			case "3":
				f.Expenditure()
			case "4":
				f.Quit()
			default:
				fmt.Println("错误的数字")
			}
		} else {
			break
		}
	}
}

// NewFamilyAccount 工厂模式
func NewFamilyAccount() *FamilyAccount {
	return &FamilyAccount{
		Balance: 10000.0,
		//每次收支的金额
		Money: 0.0,
		//每次收支的记录
		Note: "",
		//收支的详情，界面文本
		Details: "收支\t账户金额\t收支金额\t说明\n",
		//是否有收支行为
		Flag: false,
		//是否退出
		IsQuit: true,
	}
}
