package model

import "fmt"

// Customer 声明结构体信息
type Customer struct {
	Id    int
	Name  string
	Sex   string
	Age   int
	Phone string
	Email string
}

// NewCustomer 工厂模式
func NewCustomer(id int, name string, sex string, age int, phone string, email string) *Customer {
	return &Customer{
		Id:    id,
		Name:  name,
		Sex:   sex,
		Age:   age,
		Phone: phone,
		Email: email,
	}
}

func NewCustomerPlus(name string, sex string, age int, phone string, email string) *Customer {
	return &Customer{
		Name:  name,
		Sex:   sex,
		Age:   age,
		Phone: phone,
		Email: email,
	}
}

// Adduser 新增用户
func (c Customer) Adduser() Customer {
	fmt.Println("-------------------------添加客户------------------------")
	fmt.Print("Id：")
	fmt.Scan(&c.Id)
	fmt.Print("姓名：")
	fmt.Scan(&c.Name)
	fmt.Print("性别：")
	fmt.Scan(&c.Sex)
	fmt.Print("年龄：")
	fmt.Scan(&c.Age)
	fmt.Print("电话：")
	fmt.Scan(&c.Phone)
	fmt.Print("邮箱：")
	fmt.Scan(&c.Email)
	return Customer{Id: c.Id, Name: c.Name, Age: c.Age, Sex: c.Sex, Phone: c.Phone, Email: c.Email}
}

// GetInfo 获取基本信息
func (c Customer) GetInfo() string {
	return fmt.Sprintf("%v\t%v\t%v\t%v\t%v\t%v\t", c.Id, c.Name, c.Sex, c.Age, c.Phone, c.Email)
}
