package upload

import (
	"fmt"
	"net"
	"os"
)

func Check(file string) string {
	_, err := os.Stat(file)
	if err != nil {
		return "ok"
	} else {
		return "no"
	}
}

func CreateFile(conn net.Conn, file string) {
	code := Check(file)
	fmt.Println(code)
	if code == "ok" {
		Fileche, _ := os.Create(file)
		defer Fileche.Close()
		for {
			readConn(conn, Fileche)
			fmt.Println("内容写入成功")
			return
		}

	} else {
		return
	}
}

func readConn(conn net.Conn, file *os.File) {
	fmt.Println("正在读取中")
	buf := make([]byte, 20*50*1024*1024) //设置32M
	n, err := conn.Read(buf)
	if n == 0 {
		fmt.Println("读取完毕")
	}
	if err != nil {
		fmt.Println("文件读取错误")
	}
	file.Write(buf[:n])
	fmt.Println("文件写入完毕")
	file.Close()
	return
}
