package com

import (
	"flag"
	"fmt"
)

func banner() {
	banner := `
	

	/***
	*    Y88b   d88P d8b                   
	*     Y88b d88P  Y8P                   
	*      Y88o88P                         
	*       Y888P    888  .d88b.   8888b.  
	*       d888b    888 d88""88b     "88b 
	*      d88888b   888 888  888 .d888888 
	*     d88P Y88b  888 Y88..88P 888  888 
	*    d88P   Y88b 888  "Y88P"  "Y888888 
	*                                      
	*                                      
	*                                      
	*/                                                                                                           
 
						Xioa version ` + version + `
	`
	print(banner)

}

func Flag(input *Infocom) {
	banner()
	fmt.Println()
	flag.StringVar(&input.commnod, "qfn", "", "无参数取反RCE\n\texample: .\\Xioa.exe -qfn 'system(current(getallheaders()));' \n") //注意这里参数不能加入 -
	flag.StringVar(&noqufan, "qf", "", "带参数取反RCE\n\texample: .\\Xioa.exe -qf 'system(ls);' \n")
	flag.StringVar(&cat, "nocat", "", "Cat关键字被过滤的提示\n\texample: .\\Xioa.exe -nocat 1\n")
	flag.StringVar(&webshell, "webshell", "", "生成一句话websehll\n\texample: .\\Xioa.exe -webshell php1|php2|php3 \n\texample: .\\Xioa.exe -webshell jsp1|jsp2|jsp3\n\texample: .\\Xioa.exe -webshell asp1|asp2|asp3\n\t具体支持 php jsp asp\n\t简单一句话|免杀哥斯拉|冰蝎webshell\n\n")
	flag.StringVar(&msf, "msf", "", "msf的木马提示 用于快速生成木马 \n\texample: .\\Xioa.exe -msf 192.168.0.1:8008")
	flag.StringVar(&sql, "sql", "", "sql盲注简单脚本的提示 \n\t .\\Xioa.exe -sql b|t 会打印出GET|POST脚本 对应bool和time")
	flag.StringVar(&shell, "shell", "", "反弹shell的选择 \n\t .\\Xioa.exe -shell 1")
	flag.StringVar(&ssti, "ssti", "", "fenjing SSTI的python代码 \n\t .\\Xioa.exe -ssti 1")
	flag.StringVar(&nmap, "nmap", "", "nmap的扫描代码 快速使用 \n\t .\\Xioa.exe -nmap 192.168.0.1:8080")
	flag.Parse()
}
