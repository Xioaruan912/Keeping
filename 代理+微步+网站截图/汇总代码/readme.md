## 验证请求包

### 搜索认证服务

发送POST请求到`/api/search`端点：

```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password",
    "search_url": "https://example.com/search"
  }'
```

成功响应示例：

```json
{
  "message": "成功",
  "time": "5.23 s",
  "x-csrf-token": "token_value",
  "xx-csrf": "csrf_value",
  "cookie": "cookie_string"
}
```

请求包样式

```
POST /api/search HTTP/1.1
Host:127.0.0.1:5000
Content-Type: application/json
Content-Length: 95

{
"username" :"xxxx",
"password" : "xxxxx",
"search_url" : "www.baidu.com"
}
```



### 代理服务

发送请求到`/api/proxy`端点，使用自定义头部指定目标URL和代理IP：

```bash
curl -X GET http://localhost:5000/api/proxy \
  -H "target: https://example.com/api/data" \
  -H "IP: http://proxy-ip:port"
```

请求包样式

```
GET http://172.18.16.72:5000/api/proxy HTTP/1.1
Host:172.18.16.72:5000
target:http://httpbin.org/ip
IP: 代理IP
Content-Length: 2
```

## API参考

### 搜索认证服务

- **URL**: `/api/search`
- **方法**: POST
- 请求体
  - username: 用户名
  - password: 密码
  - search_url: 搜索URL
- **响应**: 认证信息(x-csrf-token, xx-csrf, cookie)

### 代理服务

- **URL**: `/api/proxy`
- **方法**: GET, POST, PUT, DELETE, PATCH, OPTIONS
- 请求头
  - target: 目标URL
  - IP: 代理IP地址
- **响应**: 转发的响应内容

## 配置文件

`setting.json` 文件包含以下配置项：

- host: 服务监听地址
- port: 服务端口
- debug: 调试模式开关

## 日志

日志文件保存在项目根目录的`app.log`中，包含详细的操作记录和错误信息。