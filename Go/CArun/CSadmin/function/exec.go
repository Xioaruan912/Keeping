
package function

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"golang.org/x/text/encoding/simplifiedchinese"
)

func GetPwd() string {
	pwd, _ := os.Getwd()
	return pwd
}

func ExecCode(shell string) string {
	test := strings.Fields(shell)
	if test[0] == "cd" && len(test) > 1 {
		output := Cd_deal(shell)
		_, _ = simplifiedchinese.GB18030.NewDecoder().String(string(output))
		return "change pwd !"
	} else {

		cmd := exec.Command("cmd.exe", "/C", shell)
		output, _ := cmd.CombinedOutput()
		out, _ := simplifiedchinese.GB18030.NewDecoder().String(string(output))
		return out
	}
}
func Cd_deal(cmd string) string {
	workingDir, _ := os.Getwd()
	parts := strings.Fields(cmd)
	if parts[0] == "cd" && len(parts) > 1 {
		newDir := parts[1]
		if newDir == "-" {
			// 处理特殊情况：切换到上一个工作目录
			workingDir, _ = os.Getwd()
		} else {
			// 将相对路径转换为绝对路径
			if !filepath.IsAbs(newDir) {
				newDir = filepath.Join(workingDir, newDir)
			}

			// 检查新目录是否存在
			_, err := os.Stat(newDir)
			if err == nil {
				workingDir = newDir
			} else {
				fmt.Println("目录不存在:", newDir)
			}
		}

		// 更新当前工作目录
		err := os.Chdir(workingDir)
		if err != nil {
			fmt.Println("切换目录失败:", err)
		}

	}
	return workingDir
}
