package rcepay

import "fmt"

var shellcode []string = []string{
	"https://www.ddosi.org/shell/", "https://forum.ywhack.com/shell.php", "https://zgao.top/reverse-shell/",
}

var jiaohu string = `
半交互：

python -c 'import pty; pty.spawn("/bin/bash")' 

`

func FMTSHELL() {
	for _, web := range shellcode {
		fmt.Println(web, "\n")
	}
	fmt.Println(jiaohu)
}
