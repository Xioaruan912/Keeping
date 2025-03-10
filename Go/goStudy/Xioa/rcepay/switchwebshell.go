package rcepay

import "fmt"

func Switchshell(payload string) {
	if payload == "php1" {
		Fmtwebshell1()
	} else if payload == "php2" {
		Gozila()
	} else if payload == "php3" {
		Binxie()
	} else if payload == "jsp1" {
		easyjsp()
	} else if payload == "jsp2" {
		GozilaJsp()
	} else if payload == "jsp3" {
		Binxiejsp()
	} else if payload == "asp1" {
		Easyasp()
	} else if payload == "asp2" {
		Gozilaasp()
	} else if payload == "asp3" {
		Binxieasp()
	} else {
		fmt.Println("还在开发哦~")
	}
}
