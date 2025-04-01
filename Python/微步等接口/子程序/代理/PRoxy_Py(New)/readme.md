## （New）PRoxy_Py	

单纯中间层转发 自动添加额外参数

### 用法

和正常的使用即可

需要额外添加

```
target  用于表示 需要请求的url
IP 用于表示代理ip
```

```
GET / HTTP/1.1
Host: 172.18.16.72:5000
target : https://baidu.com   // 需要通过代理访问的网站
IP:http://127.0.0.1:7897	// 用户传入的代理IP
```

即可发送代理访问 主要参数如下

如果需要其他参数 添加在请求头即可

```
target: https://baidu.com
IP: 代理
其他特殊头
```

通过`rebuild` 重构请求头 需要排除的 添加在 `excluded` 中 就不会被转发

```
def rebuild_headers(headers):
    """重建请求头，去除一些特殊头部"""
    excluded_headers = [
        'content-encoding',
        'content-length',
        'transfer-encoding',
        'connection',
        'host',
        'target',
        'ip',
    ]
    filtered_headers = {
        key: value for key, value in headers.items()
        if key.lower() not in excluded_headers
    }
    print("过滤后的头部信息:", filtered_headers)

    return filtered_headers
```

# 验证代理

```
GET http://172.18.16.72:5000/ HTTP/1.1
Host:172.18.16.72:5000
target:http://httpbin.org/ip
IP:127.0.0.1:7897
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
```

# app.log

日志

# setting.json

```
{
    "host": "0.0.0.0", // ip
    "port": 5000,	// 端口
    "debug": false
}
```

