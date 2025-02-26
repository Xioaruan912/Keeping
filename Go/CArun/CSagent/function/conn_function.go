package function

import (
	"fmt"
	"net"
)

func Conn_net() net.Conn {
	ip := "127.0.0.1"
	port := "123"
	ipaddr := fmt.Sprintf("%v:%v", ip, port)
	for {
		conn, err := net.Dial("tcp", ipaddr)
		if err == nil {
			return conn
		}
		return conn
	}
}

func Lis_net(port string) net.Conn {
	new_port := ":" + port
	lis, err := net.Listen("tcp", new_port)
	if err != nil {
		fmt.Println("监听错误")
	}
	fmt.Printf("开始监听 > %v", port)
	conn, _ := lis.Accept()
	return conn
}

func Read_conn(conn net.Conn) (string, error) {
	buf := make([]byte, 512)
	n, err := conn.Read(buf)
	if err != nil {
		fmt.Println("读取错误")
	}
	// fmt.Println(n)
	output := string(buf[:n])
	fmt.Println("output:", output)
	return output, err
}
func Write_conn(conn net.Conn, str string) {
	_, _ = conn.Write([]byte(str))
}
