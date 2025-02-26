import random
from loguru import logger
import requests
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main_get_request(url, proxy):
    # 设置代理

    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    # proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0',
    }

    logger.info("开始发送请求")
    # 发送请求
    response = requests.get(
        url,
        proxies=proxies,
        headers=headers,
        verify=False,
        allow_redirects=True  # 允许重定向
    )
    logger.info(response.text)
    return response.text

