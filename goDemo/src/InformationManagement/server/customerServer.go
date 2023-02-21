package server

import (
	"InformationManagement/model"
	"fmt"
)

// CustomerServer 结构体
type CustomerServer struct {
	customers []model.Customer
	// 自增id
	customerNum int
}

// NewCustomerServer 工厂模式
func NewCustomerServer() *CustomerServer {
	customerServe := &CustomerServer{}
	customerServe.customerNum = 1
	customer := model.NewCustomer(1, "Tom", "男", 10, "135", "444")
	customerServe.customers = append(customerServe.customers, *customer)
	return customerServe
}

// Add 新增用户
func (cs *CustomerServer) Add(customer model.Customer) bool {
	cs.customerNum++
	customer.Id = cs.customerNum
	cs.customers = append(cs.customers, customer)
	return true
}

func (cs *CustomerServer) UpdateUser(index int) bool {
	_index := cs.GetCustomersIndex(index)
	if _index == -1 {
		fmt.Print("修改的id不存在")
		return false
	} else {
		item := cs.customers[_index]
		fmt.Printf("姓名（%v）：", item.Name)
		fmt.Scan(&item.Name)
		fmt.Printf("性别（%v）：", item.Sex)
		fmt.Scan(&item.Sex)
		fmt.Printf("年龄（%v）：", item.Age)
		fmt.Scan(&item.Age)
		fmt.Printf("电话（%v）：", item.Phone)
		fmt.Scan(&item.Phone)
		fmt.Printf("邮箱（%v）：", item.Email)
		fmt.Scan(&item.Email)
		cs.customers[_index] = item
		return true
	}
}

// DeleteUser 删除客户信息
func (cs *CustomerServer) DeleteUser(index int) bool {
	_index := cs.GetCustomersIndex(index)
	if _index == -1 {
		fmt.Print("删除的id不存在")
		return false
	} else {
		// 切片结构体
		cs.customers = append(cs.customers[:_index], cs.customers[_index+1:]...)
		return true
	}
}

// GetCustomersIndex 获取切片结构体列表
func (cs CustomerServer) GetCustomersIndex(id int) int {
	for _index, value := range cs.customers {
		if value.Id == id {
			return _index
		}
	}
	return -1
}

// List 获取用户列表详情
func (cs CustomerServer) List() []model.Customer {
	return cs.customers
}
