package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	fmt.Println("客户端启动")
	conn, err := net.Dial("tcp", "127.0.0.1:8888")
	if err != nil {
		fmt.Println("出错")
	} else {
		fmt.Println("成功", conn.RemoteAddr().String())
	}
	//通过客户端发送单行的数据
	reader := bufio.NewReader(os.Stdin) //标准输入
	str, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("接受失败")
	}
	//发送服务端
	n, err := conn.Write([]byte(str))
	if err != nil {
		fmt.Println("错误")
	}
	fmt.Printf("数据发送了%v字节", n)
}
