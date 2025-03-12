import os

import requests
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_proxy_config(proxy=None):
    """
    获取代理配置（优先级：参数 > 环境变量 > 无代理）

    :param proxy: 外部传入的代理地址（格式：IP:Port 或 http://IP:Port）
    :return: 代理配置字典，如 {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
    """
    # 优先级：外部参数 > 环境变量
    proxy = proxy or os.environ.get('GLOBAL_PROXY')
    if not proxy:
        return None

    # 自动补全协议头
    if not proxy.startswith(('http://', 'https://')):
        proxy = f"http://{proxy}"  # 默认使用 HTTP 协议

    return {
        "http": proxy,
        "https": proxy
    }


def fix_url_protocol(url, proxy):
    """自动补全 URL 协议（HTTP/HTTPS）"""
    if not url.startswith(('http://', 'https://')):
        logger.info(f"尝试补全协议: {url}")
        # 尝试 HTTP 和 HTTPS
        for protocol in ['http://', 'https://']:
            test_url = f"{protocol}{url}"
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
                }
                response = requests.get(test_url, headers=headers, proxies=get_proxy_config(proxy), timeout=5)
                if 200 <= response.status_code < 400:
                    logger.info(f"可用协议: {test_url}")
                    return test_url
            except requests.RequestException:
                continue
        logger.error("HTTP/HTTPS 均不可用")
        return None
    return url


