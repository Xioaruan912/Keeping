## （New）PRoxy_Py	

单纯中间层转发 自动添加额外参数

### 用法

和正常的使用即可

需要额外添加

```
Original-Url  用于表示 需要请求的url
IP 用于表示代理ip
```

```
GET / HTTP/1.1
Host: 172.18.16.72:5000
Upgrade-Insecure-Requests: 1
Original-Url : https://baidu.com
IP:http://127.0.0.1:7897
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
```

即可发送代理访问