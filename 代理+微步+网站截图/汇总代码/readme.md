```
.
├── app.py   //接口主程序
├── function // 微步
│   ├── Cycheck.py  //处理拖拽运动函数
│   ├── main_request.py //主要请求函数
│   └── openChrome.py  //driver设置函数
├── picture_function
│   ├── openChrome.py  //driver设置函数
│   └── picture_get.py //截图icon处理函数
├── proxy		
│   └── proxy.py 	  // 代理处理函数
└── web_scan   	
│   └── WebsiteScanner.py //网站扫描处理函数
└── Get_100
    └── Get_100.py   //百万网站函数
```

树状图如上

打包指令

```
pip install pyinstaller 
pyinstaller --onefile --hidden-import=requests.adapters --hidden-import=urllib3 --clean --add-data=libzbar-64.dll:./pyzbar/ --add-data=libiconv.dll:./pyzbar/  app.py
```



# API 接口文档

## 概述

本文档描述了服务提供的 API 接口，包括网站扫描、网站截图、图标提取、搜索认证和代理服务等功能。

## 基本信息

- 基础URL: 根据配置文件中的 host 和 port 决定，默认为 `http://0.0.0.0:5000`
- 所有 POST 请求的数据格式为 JSON
- 所有响应均为 JSON 格式，除非特别说明

## 接口列表

### 1. 网站扫描接口

扫描指定网站并返回扫描结果。

- **URL**: `/api/scan`
- **方法**: `POST`
- **请求参数**:

| 参数名 | 类型   | 必填 | 描述            |
| :----- | :----- | :--- | :-------------- |
| url    | string | 是   | 要扫描的网站URL |

- **请求示例**:

```json
{
  "url": "https://example.com"
}
```

- 响应:
  - 成功: 返回扫描结果，状态码 200
  - 失败: 返回错误信息，状态码 400

### 2. 百万网站获取接口

获取百万网站数据并存入数据库。

- **URL**: `/api/get100`
- **方法**: `POST`
- **请求参数**:

| 参数名    | 类型   | 必填 | 描述    |
| :-------- | :----- | :--- | :------ |
| API_TOKEN | string | 是   | API令牌 |

- **请求示例**:

```json
{
  "API_TOKEN": "your_api_token_here"
}
```

- 响应:
  - 成功: 返回"成功"，状态码 200
  - 失败: 返回错误信息，状态码 400

### 3. 网站截图接口

对指定网站进行截图并返回图片。

- **URL**: `/api/capture`
- **方法**: `POST`
- **请求参数**:

| 参数名 | 类型   | 必填 | 描述            |
| :----- | :----- | :--- | :-------------- |
| url    | string | 是   | 要截图的网站URL |
| proxy  | string | 否   | 代理服务器地址  |

- **请求示例**:

```json
{
  "url": "https://example.com",
  "proxy": "http://127.0.0.1:8080"
}
```

- 响应:
  - 成功: 返回PNG格式的图片数据，Content-Type 为 image/png
  - 失败: 返回错误信息，状态码 400 或 500

### 4. 网站图标提取接口

提取指定网站的图标并返回Base64编码的图标数据。

- **URL**: `/api/icon`
- **方法**: `POST`
- **请求参数**:

| 参数名 | 类型   | 必填 | 描述                |
| :----- | :----- | :--- | :------------------ |
| url    | string | 是   | 要提取图标的网站URL |
| proxy  | string | 否   | 代理服务器地址      |

- **请求示例**:

```json
{
  "url": "https://example.com",
  "proxy": "http://127.0.0.1:8080"
}
```

- 响应:

  - 成功:

  ```json
  {
    "status": "success",
    "data": "base64_encoded_icon_data"
  }
  ```

  - 失败: 返回错误信息，状态码 400、404 或 500

### 5. 搜索认证服务接口

执行搜索认证并返回认证信息。

- **URL**: `/api/search`
- **方法**: `POST`
- **请求参数**:

| 参数名     | 类型   | 必填 | 描述    |
| :--------- | :----- | :--- | :------ |
| username   | string | 是   | 用户名  |
| password   | string | 是   | 密码    |
| search_url | string | 是   | 搜索URL |

- **请求示例**:

```json
{
  "username": "your_username",
  "password": "your_password",
  "search_url": "https://example.com/search"
}
```

- 响应:

  - 成功:

  ```json
  {
    "message": "成功",
    "time": "1.23 s",
    "x-csrf-token": "token_value",
    "xx-csrf": "csrf_value",
    "cookie": "cookie_value"
  }
  ```

  - 失败: 返回错误信息，状态码 400 或 500

### 6. 代理服务接口

提供HTTP请求代理功能。

- **URL**: `/api/proxy`
- **方法**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `OPTIONS`
- **请求头**:

| 头部名称 | 必填 | 描述           |
| :------- | :--- | :------------- |
| target   | 是   | 目标URL        |
| IP       | 是   | 代理服务器地址 |

- 响应:
  - 成功: 返回代理请求的响应内容和状态码
  - 失败: 返回错误信息，状态码 400 或 500

## 错误处理

所有接口在发生错误时都会返回相应的错误信息和HTTP状态码：

- 400: 请求参数错误
- 404: 资源不存在
- 500: 服务器内部错误

## 注意事项

1. 所有接口调用前请确保服务已正常启动
2. 代理服务和截图服务可能受网络环境影响
3. 百万网站获取接口需要有效的API令牌
4. 详细的错误信息可在服务器日志中查看

# app.py

## `扫描接口`

```python
@app.route('/api/scan', methods=['POST'])
def scan():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': '缺少 "url" 参数'}), 400

    target_url = data['url']

    scanner = WebsiteScanner(target_url)
    results = scanner.scan_website()

    return jsonify(results), 200

```

要求传递 `url` 然后调用  `网站扫描处理函数` 执行网站扫描

## `截图接口`

```c
@app.route('/api/capture', methods=['POST'])
def capture_website_screenshot():
    """截图指定网页并返回 PNG 图片"""
    try:
        data = request.json
        url = data.get('url')
        proxy = data.get('proxy')

        if not url:
            logger.error("缺少必要参数: url")
            return jsonify({"error": "Missing 'url'"}), 400

        # 补全协议
        fixed_url = fix_url_protocol(url, proxy)
        if not fixed_url:
            return jsonify({"error": "URL 不可访问"}), 400

        # 初始化浏览器
        driver = open_Chrome_pic(proxy)
        try:
            logger.info(f"访问 URL: {fixed_url}")
            driver.get(fixed_url)
            time.sleep(5)  # 等待页面加载
            driver.set_window_size(1920, 1080)
            screenshot_data = driver.get_screenshot_as_png()

            # 构造响应
            response = make_response(screenshot_data)
            response.headers.set('Content-Type', 'image/png')
            response.headers.set('Content-Disposition', 'attachment', filename='screenshot.png')
            return response
        except Exception as e:
            logger.error(f"截图失败: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            driver.quit()
    except Exception as e:
        logger.error(f"全局异常: {str(e)}")
        return jsonify({"error": "服务器错误"}), 500


```

```
1. 初始化 driver 
2. 传递必要参数 url 和 不必要参数 proxy
3. 补全url
4. 执行截图函数 get_screenshot_as_png 这个是selenium 自带函数
```

## `Icon提取接口`

```python
@app.route('/api/icon', methods=['POST'])
def extract_icon_elements():
    try:
        data = request.json
        url = data.get('url')
        proxy = data.get('proxy')

        if not url:
            return jsonify({"error": "Missing 'url'"}), 400

        fixed_url = fix_url_protocol(url, proxy)
        if not fixed_url:
            return jsonify({"error": "URL 不可访问"}), 400

        driver = open_Chrome_pic(proxy)
        try:
            logger.info(f"正在提取图标: {fixed_url}")
            driver.get(fixed_url)

            # 等待页面加载完成
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            logger.info("页面加载完成")

            # 解析页面获取图标URL
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            icon_link = soup.find("link", rel=lambda x: x and x in ["icon", "shortcut icon"])
            icon_url = urljoin(fixed_url, icon_link['href']) if icon_link else urljoin(fixed_url, '/favicon.ico')
            logger.info(f"图标地址: {icon_url}")

            # 使用 driver 加载图标
            driver.get(icon_url)

            # 等待图标加载完成
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            logger.info("图标加载完成")

            # 获取图标的 Base64 编码
            icon_base64 = driver.execute_script("""
                var canvas = document.createElement('canvas');
                var img = document.querySelector('img');
                if (!img) return null;

                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;
                var ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);

                return canvas.toDataURL('image/png').split(',')[1];
            """)

            if icon_base64:
                return jsonify({
                    "status": "success",
                    "data": icon_base64
                })
            else:
                logger.error("未找到图标元素")
                return jsonify({"error": "未找到图标元素"}), 404

        except Exception as e:
            logger.error(f"图标提取失败: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            driver.quit()
    except Exception as e:
        logger.error(f"全局异常: {str(e)}")
        return jsonify({"error": "服务器错误"}), 500

```

```
1. 初始化 driver
2. 解析页面获取图标URL
```

## `微步认证接口`

```python
@app.route('/api/search', methods=['POST'])
def run_script():
    """搜索认证服务路由"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    search_url = data.get('search_url')

    if not username or not password or not search_url:
        return jsonify({"error": "缺少用户名、密码或搜索链接"}), 400

    try:
        start_time = time.time()
        driver = open_Chrome(username, password)
        if driver == None:
            return jsonify({"error": "check app.log"}), 500
        bypass(driver, "/html/body/div[3]/div[2]/div/div[2]/div/div/div[1]/div[1]/div[1]",
               "/html/body/div[3]/div[2]/div/div[2]/div/div/div[1]/div[2]",
               "/html/body/div[3]/div[2]/div/div[2]/div/div/div[1]/div[1]/div[1]")
        search_req(driver, search_url)
        x_csrf_token, xx_csrf, cookie = get_auth(driver)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"脚本执行时间: {elapsed_time:.2f} 秒")
        return jsonify({
            "message": "成功",
            "time": f"{elapsed_time:.2f} s",
            "x-csrf-token": x_csrf_token,
            "xx-csrf": xx_csrf,
            "cookie": cookie
        }), 200
    except Exception as e:
        logger.error(f"发生错误: {e}")
        logger.info("发生 查看日志")
        return jsonify({"error": "check app.log"}), 500
```

```
1. 接受必要参数
2. 初始化driver  并且执行登入
3. 执行反爬虫绕过机制
4. 获取返回包的token
```

## `代理接口`

```python
@app.route('/api/proxy', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy():
    """代理服务路由"""
    try:
        original_url = request.headers.get('target')
        ip = request.headers.get('IP')
        if not original_url:
            logger.error("缺少 target 头部")
            return "缺少 target 头部", 400
        if not ip:
            logger.error("缺少 IP 头部")
            return "缺少 IP 头部", 400

        method = request.method
        headers = rebuild_headers(dict(request.headers))
        headers = add_browser_headers(headers)

        data = request.get_data() if method != 'GET' else None
        params = request.args

        proxies = {'http': ip, 'https': ip}
        now_time = time.time()
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_time))
        logger.info(f"=============时间：{formatted_time}============")
        logger.info(f"转发 {method} 请求到: {original_url}")
        logger.info(f"使用代理: {proxies}")
        logger.info(f"使用头: {headers}")
        time.sleep(random.uniform(0.5, 2))

        response = requests.request(method=method, url=original_url, headers=headers, data=data, params=params,
                                    proxies=proxies, verify=False, allow_redirects=True, timeout=30)
        proxy_response = Response(response.content, status=response.status_code)

        response_headers = rebuild_headers(dict(response.headers))
        for key, value in response_headers.items():
            proxy_response.headers[key] = value

        logger.info(f"响应状态: {response.status_code}")

        if response.headers.get('Content-Type') == 'application/json':
            response_data = response.json()
            response_data['new_field'] = '新值'
            proxy_response.set_data(json.dumps(response_data))
        return proxy_response

    except requests.exceptions.RequestException as e:
        logger.error(f"请求失败: {str(e)}")
        return str(e), 500
    except Exception as e:
        logger.error(f"意外错误: {str(e)}")
        return str(e), 500


```

```
        headers = rebuild_headers(dict(request.headers))
        headers = add_browser_headers(headers)
        构造请求头 和 继承请求头
        
        最后直接通过代理转发
```

# function  ---- 李昕泽

## Cvcheck.py

```
运动函数 模拟拖拽 传递图片 一个是 缺口图片 一个是滑块图片 然后进行 cv计算 获取距离
```

## main_request.py

### `deal_img`

识别和提取滑块+缺口函数

### `download_image`

下载函数到本地

### `main_req_func`

登入逻辑处理 包括错误验证 账号密码错误 并且存在 滑块失误处理

### `search_req`

处理搜索方法

### `bypass`

反爬虫机制绕过

### `get_auth`

头中获取必要数值

## openChrome.py

### `open_Chrome`

driver必要参数  并且执行 登入函数

# picture_function  ---- 蔡子泓

## openChrome.py

### `open_Chrome_pic`

driver必要参数  并且执行 登入函数

## picture_get.py

### `get_proxy_config`

配置代理

### `fix_url_protocol`

补全http/s头

# proxy ---- 李昕泽

## proxy.py

### `rebuild_headers`

重建头 里面可以添加 不重建的头

### `get_random_ua`

随机ua

### `add_browser_headers`

添加随机参数  反爬虫机制绕过

# web_scan ---- 李昕泽

## WebsiteScanner.py

### `scan_qr_code`

传递过来图片全部进行 解码

### `find_download_links`

查找下载链接 通过匹配

### `process_images`

查找图片	

### `crawl_page`

爬取页面

`scan_website`

网站扫描流程

# Get_100 ---- 张权

## Get_100.py

获取百万数据 