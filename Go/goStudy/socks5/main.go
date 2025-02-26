package main

import (
	"bufio"
	"context"
	"encoding/binary"
	"fmt"
	"io"
	"log"
	"net"
)

const ipv4 = 0x01
const url = 0x03
const vercheck = 0x05 // socks5版本号

func main() {
	client, err := net.Listen("tcp", "127.0.0.1:1080")
	if err != nil {
		log.Printf("client 127.0.0.1:1080 error:", err)
	}
	for {
		conn, err := client.Accept()
		if err != nil {
			log.Printf("accpect error:", err)
		}
		go process(conn)
	}
}

func process(conn net.Conn) {
	defer conn.Close()
	reader := bufio.NewReader(conn)
	err := auth(reader, conn) //实现完认证 该实现读取报文
	if err != nil {
		log.Printf("auth error:", err)
	}
	err = connect(reader, conn)
	if err != nil {
		log.Printf("connect error:", err)
	}
}

func auth(reader *bufio.Reader, conn net.Conn) (err error) { //开始认证
	verNum, err := reader.ReadByte() // 读取一个字节
	if verNum != vercheck {
		fmt.Println("not socks5")
		return
	}
	mothodSize, _ := reader.ReadByte()
	mothod := make([]byte, mothodSize)
	// fmt.Println(reader)  从fmt可以发现  5 1 0 0 0 0 这一次的报文是 5 1 所以对应的就是 ver 和 mothod
	_, err = io.ReadFull(reader, mothod)        //这里是将reader中字节流存入 mothod
	_, err = conn.Write([]byte{vercheck, 0x00}) //然后再从链接中写入版本号 和 不认证 来进行 类似 握手的
	return nil
}
func connect(reader *bufio.Reader, conn net.Conn) (err error) { //开始认证
	// +----+-----+-------+------+----------+----------+
	// |VER | CMD |  RSV  | ATYP | DST.ADDR | DST.PORT |
	// +----+-----+-------+------+----------+----------+
	// | 1  |  1  | X'00' |  1   | Variable |    2     |
	// +----+-----+-------+------+----------+----------+
	buf := make([]byte, 4)
	_, err = io.ReadFull(reader, buf)
	// fmt.Println(buf)
	var ver1, cmd, atyp = buf[0], buf[1], buf[3]
	if ver1 != vercheck {
		return fmt.Errorf("ver")
	}
	if cmd != 1 {
		return fmt.Errorf("cmd")
	}

	addr := ""
	switch atyp {
	case ipv4:
		_, _ = io.ReadFull(reader, buf)
		addr = fmt.Sprintf("%d.%d.%d.%d", buf[0], buf[1], buf[2], buf[3])
	case url:
		urlsize, _ := reader.ReadByte()
		urlcheck := make([]byte, urlsize)
		_, _ = io.ReadFull(reader, urlcheck)
		addr = string(urlcheck)
	default:
		fmt.Println("not yet")
	}
	_, err = io.ReadFull(reader, buf[:2])
	if err != nil {
		return fmt.Errorf("read port failed:%w", err)
	}
	port := binary.BigEndian.Uint16(buf[:2])
	dest, err := net.Dial("tcp", fmt.Sprintf("%v:%v", addr, port))
	defer dest.Close()
	fmt.Println("获取到", addr, port)
	_, _ = conn.Write([]byte{0x05, 0x00, 0x00, 0x01, 0, 0, 0, 0, 0, 0})
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	go func() {
		_, _ = io.Copy(dest, reader)
		cancel()
	}()
	go func() {
		_, _ = io.Copy(conn, dest)
		cancel()
	}()
	<-ctx.Done()
	return nil
}
