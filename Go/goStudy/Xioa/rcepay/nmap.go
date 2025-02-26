package rcepay

import (
	"fmt"
	"os"
	"regexp"
)

var NmapString_p_1_65536_speed string = `nmap -sS -Pn -n --open --min-hostgroup 4 -p- --min-parallelism 1024 --host-timeout 30 -T4 -v -oG result.txt %v`
var NmapString_p_system string = `nmap -T4 -A %v`
var NmapCscan string = `Nmap -sn -PE -n %v/24  或者 nmap -v -sP %v/24  `

func NmapMain(nmap string) {
	check(nmap)
}

func check(s string) {
	re, err := regexp.Compile("^(((25[0-5]|2[0-4]d|((1\\d{2})|([1-9]?\\d)))\\.){3}(25[0-5]|2[0-4]\\d|((1\\d{2})|([1-9]?\\d))))")
	if err != nil {
		fmt.Println("出现错误")
		os.Exit(0)
	}
	rep := re.FindString(s)
	fmt.Println("全端口快速扫描:")
	fmt.Printf(NmapString_p_1_65536_speed, rep)
	fmt.Println("\n")
	fmt.Println("1-10000端口扫描，操作系统探测，路由跟踪，服务探测:")
	fmt.Printf(NmapString_p_system, rep)
	fmt.Println("\n")
	fmt.Println("扫描C段主机存活:")
	fmt.Printf(NmapCscan, rep, rep)
	fmt.Println("\n")
}
