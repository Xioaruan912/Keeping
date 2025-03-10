package com

import (
	"Xioa/rcepay"
	"fmt"
	"os"
	"strings"

	"github.com/fatih/color"
)

func Parse(Info *Infocom) {
	// fmt.Println(Info)
	norce()
	Parsepayload(Info)
	wherecat()
	wherewebshell()
	msfcheck()
	sql2()
	shellpares()
	checkssti()
	nmapcheck()
}

func Parsepayload(payload *Infocom) { // 无参数的rce 无数字字母
	red := color.New(color.FgGreen).PrintfFunc()
	payloadStr := fmt.Sprintf("%v", *payload) // 将*Infocom类型的payload转换为字符串类型
	payloadStr = RemoveBraces(payloadStr)
	// fmt.Println(payloadStr)
	// fmt.Println(payloadStr)
	// fmt.Println(payloadStr)
	if payload.commnod != "" {
		a := rcepay.Execute(&payload.commnod) // 传递payload.commnod的地址
		red("\n\n\n\n\npayload为:%v", a)

	}
}

func norce() { // 有参数的rce 无数字字母
	if noqufan != "" {
		res := rcepay.HaveRce(noqufan)
		fmt.Println("payload为 :", res)

	}
}

func RemoveBraces(code string) string {
	// 使用 strings 包的 Replace 方法将 "{" 和 "}" 替换为空字符串
	code = strings.ReplaceAll(code, "{", "")
	code = strings.ReplaceAll(code, "}", "")
	return code
}

func wherecat() {
	if cat == "1" {
		rcepay.Nocat1()
	}
}

func wherewebshell() {
	if webshell != "" {
		rcepay.Switchshell(webshell)
	}
}

func msfcheck() {
	if msf != "" {
		rcepay.MsfSwitch(msf)
	}
}
func sql2() {
	if sql != "" {
		if sql == "b" || sql == "B" {
			rcepay.Bool()
		} else if sql == "t" || sql == "T" {
			rcepay.Time()
		} else {
			fmt.Println("输入错误！！")
			os.Exit(0)
		}
	}
}

func shellpares() {
	if shell != "" {
		rcepay.FMTSHELL()
	}
}

func checkssti() {
	if ssti != "" {
		rcepay.FMTSSTI()
	}
}

func nmapcheck() {
	if nmap != "" {
		rcepay.NmapMain(nmap)
	}
}
