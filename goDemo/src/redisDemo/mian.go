package main

import (
	"fmt"
	"github.com/gomodule/redigo/redis"
	"reflect"
)

var pool *redis.Pool

func init() {
	pool = &redis.Pool{
		MaxIdle:     8,   // 最大空闲连接数,数量不够的时候，动态新增
		MaxActive:   0,   // 标识和数据库的最大连接数 0：表示没有限制
		IdleTimeout: 100, // 最大空闲时间
		Dial: func() (redis.Conn, error) {
			return redis.Dial("tcp", "localhost:6379")
		},
	}
}
func main() {

	// 先取出一个连接
	coon := pool.Get()

	defer coon.Close()

	_, err := coon.Do("set", "name", "汤姆猫")
	if err != nil {
		fmt.Println("操作失败")
		return
	}
	name, _ := redis.String(coon.Do("get", "name"))
	fmt.Println("name", name, reflect.TypeOf(name))

}
