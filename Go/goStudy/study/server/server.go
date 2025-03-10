package main

import (
	"fmt"
	"net"
)

func process(conn net.Conn) {

	for {
		buf := make([]byte, 1024)
		n, err := conn.Read(buf)
		if err != nil {
			fmt.Println("读取错误:", err)
			return
		}
		fmt.Println("读取到的内容为：", string(buf[:n]))
	}
}

func main() {
	fmt.Println("服务端启动...")
	listen, err := net.Listen("tcp", "127.0.0.1:8888")
	if err != nil {
		fmt.Println("监听失败:", err)
		return
	}

	conn, err := listen.Accept()
	if err != nil {
		fmt.Println("接受客户端连接失败:", err)
		return
	}
	fmt.Println("客户端连接成功:", conn.RemoteAddr().String())
	process(conn)
	defer conn.Close()
}
