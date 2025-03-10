package main

import (
	"Xioa/com"
)

func main() {
	var payload com.Infocom
	// 定义命令行标志
	com.Flag(&payload)
	// 解析命令行参数
	com.Parse(&payload)
}
