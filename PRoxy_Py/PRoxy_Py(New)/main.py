import sys
from flask import Flask, request, Response
import requests
from loguru import logger

app = Flask(__name__)


def rebuild_headers(headers):
    """重建请求头，去除一些特殊头部"""
    excluded_headers = [
        'content-encoding',
        'content-length',
        'transfer-encoding',
        'connection',
        'host'
    ]
    return {
        key: value for key, value in headers.items()
        if key.lower() not in excluded_headers
    }

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy(path):
    try:
        original_url = request.headers.get('Original-Url')
        ip = request.headers.get('IP')
        if not original_url:
            logger.error("缺少 Original-Url 头部")
            return "缺少 Original-Url 头部", 400
        if not ip:
            logger.error("缺少 IP 头部")
            return "缺少 IP 头部", 400

        method = request.method
        headers = rebuild_headers(dict(request.headers))
        data = request.get_data() if method != 'GET' else None  # 仅在非GET请求时获取数据
        params = request.args

        proxies = {
            'http': ip,
            'https': ip
        }

        logger.info(f"转发 {method} 请求到: {original_url}")
        logger.info(f"使用代理: {proxies}")
        logger.info(f"请求头: {headers}")
        logger.debug(f"请求体: {data}")
        logger.debug(f"请求参数: {params}")

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
        logger.debug(f"响应头: {response_headers}")

        if response.headers.get('Content-Type') == 'application/json':
            import json
            response_data = response.json()
            response_data['new_field'] = '新值'
            proxy_response.set_data(json.dumps(response_data))
            proxy_response.headers['Content-Type'] = 'application/json'

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
    app.run(host='0.0.0.0', port=5000, debug=True)