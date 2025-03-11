import json
import os
import random
import time
from flask import Flask, jsonify, request, Response
import requests
from loguru import logger

from function.main_request import search_req, get_auth, bypass
from function.openChrome import  open_Chrome

# 创建Flask应用
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# 配置日志
def setup_logger():
    try:
        log_file_path = os.path.join(os.getcwd(), "app.log")
        logger.add(log_file_path, rotation="1 MB", retention="10 days", compression="zip", encoding="utf-8")
        logger.info("日志配置成功，日志文件路径: {}", log_file_path)
    except Exception as e:
        print(f"日志配置失败: {e}")

# 读取配置文件
def read_setting_json():
    current_dir = os.getcwd()
    config_path = os.path.join(current_dir, 'setting.json')

    default_config = {
        'host': '0.0.0.0',
        'port': 5000,
        'debug': False
    }

    try:
        if os.path.exists(config_path):
            logger.success(f"配置文件存在：{config_path}")
            with open(config_path, 'r') as f:
                config = json.load(f)
            return {
                'host': config.get('host', default_config['host']),
                'port': config.get('port', default_config['port']),
                'debug': config.get('debug', default_config['debug'])
            }
        else:
            logger.info("配置文件不存在，创建配置文件并使用默认配置。")
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            logger.success(f"已创建配置文件：{config_path}")
            return default_config
    except Exception as e:
        logger.error(f"读取配置文件出错: {str(e)}，启动默认配置")
        return default_config

# 设置请求头
def rebuild_headers(headers):
    excluded_headers = [
        'content-encoding', 'content-length', 'transfer-encoding',
        'connection', 'host', 'target', 'ip',
    ]
    return {key: value for key, value in headers.items() if key.lower() not in excluded_headers}

def get_random_ua():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
    ]
    return random.choice(user_agents)

def add_browser_headers(headers):
    common_headers = {
        'User-Agent': get_random_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0'
    }
    merged_headers = common_headers.copy()
    merged_headers.update(headers)
    return merged_headers

# 路由定义
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

# 错误处理
@app.errorhandler(404)
def not_found(e):
    logger.warning("404 错误: 找不到")
    return "找不到", 404

@app.errorhandler(500)
def internal_error(e):
    logger.error("500 错误: 内部服务器错误")
    return "内部服务器错误", 500

if __name__ == '__main__':
    setup_logger()
    config = read_setting_json()
    app.config['JSON_SORT_KEYS'] = False  # 禁止排序
    app.run(host=config['host'], port=config['port'], debug=config['debug'])