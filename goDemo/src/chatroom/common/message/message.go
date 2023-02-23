package message

const (
	LoginMesType = "LoginMes"
	LoginResType = "LoginRes"
)

type Message struct {
	Type string `json:"type"` // 消息类型
	Data string `json:"data"` //消息数据
}

type LoginMes struct {
	UserId   int    `json:"userId"`   //用户id
	UserPwd  string `json:"userPwd"`  //用户密码
	UserName string `json:"UserName"` // 用户名
}

type LoginRes struct {
	Code  int    `json:"code"`  // 自定义状态码 500:用户未注册 200：登陆成功
	Error string `json:"error"` // 错误信息
}
