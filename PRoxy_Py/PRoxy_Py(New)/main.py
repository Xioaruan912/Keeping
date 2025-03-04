import json
import os
import random
import time
import urllib3
from flask import Flask, request, Response
import requests
from loguru import logger


try:
    # 使用绝对路径确保日志文件写入正确的位置
    log_file_path = os.path.join(os.getcwd(), "app.log")
    logger.add(log_file_path, rotation="1 MB", retention="10 days", compression="zip", encoding="utf-8")
    logger.info("日志配置成功，日志文件路径: {}", log_file_path)
except Exception as e:
    print(f"日志配置失败: {e}")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = Flask(__name__)
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

    return filtered_headers


def read_setting_json():
    # 获取当前工作目录
    current_dir = os.getcwd()
    config_path = os.path.join(current_dir, 'setting.json')

    # 默认配置
    default_config = {
        'host': '0.0.0.0',
        'port': 5000,
        'debug': False
    }

    try:
        # 尝试读取配置文件
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


def get_random_ua():
    """返回随机User-Agent"""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
    ]
    return random.choice(user_agents)


def add_browser_headers(headers):
    """添加浏览器常见请求头"""
    common_headers = {
        'User-Agent': get_random_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache'
    }

    # 更新headers，保留原有的自定义头部
    merged_headers = common_headers.copy()
    merged_headers.update(headers)
    return merged_headers


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy(path):
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
        # 添加浏览器特征头部
        headers = add_browser_headers(headers)

        data = request.get_data() if method != 'GET' else None  # 仅在非GET请求时获取数据
        params = request.args

        proxies = {
            'http': ip,
            'https': ip
        }
        now_time = time.time()
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_time))
        logger.info(f"=============时间：{formatted_time}============")
        logger.info(f"转发 {method} 请求到: {original_url}")
        logger.info(f"使用代理: {proxies}")
        logger.info(f"使用头: {headers}")
        # 添加随机延时
        time.sleep(random.uniform(0.5, 2))

        response = requests.request(
            method=method,
            url=original_url,
            headers=headers,
            data=data,
            params=params,
            proxies=proxies,
            verify=False,
            allow_redirects=True,
            timeout=30
        )
        proxy_response = Response(
            response.content,
            status=response.status_code
        )

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
    config = read_setting_json()
    app.run(
        host=config['host'],
        port=config['port'],
        debug=config['debug']
    )