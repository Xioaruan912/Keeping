package function

import (
	"fmt"
	"net"
	"os"
)

func Conn_net(ip string, port string) net.Conn {

	ipaddr := fmt.Sprintf("%v:%v", ip, port)
	lis, err := net.Dial("tcp", ipaddr)
	if err != nil {
		fmt.Println("链接错误")
		os.Exit(0)
	}
	return lis
}

func Lis_net(port string) net.Conn {
	// time.Sleep(time.Second * 2)
	new_port := ":" + port
	lis, err := net.Listen("tcp", new_port)
	if err != nil {
		fmt.Println("监听错误", err)
		os.Exit(0)
	}
	fmt.Printf("开始监听 > %v\n", port)
	conn, _ := lis.Accept()
	return conn
}

func Read_conn(conn net.Conn) string {
	buf := make([]byte, 20*50*1024*1024)
	n, err := conn.Read(buf)
	if err != nil {
		fmt.Println("读取错误")
		os.Exit(0)
	}
	output := string(buf[:n])
	return output
}
func Write_conn(conn net.Conn, str string) {
	_, _ = conn.Write([]byte(str))
}
