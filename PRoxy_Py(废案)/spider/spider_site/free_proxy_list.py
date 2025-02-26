import re
from loguru import logger
import requests


def free_proxy_list():
    proxies = {
        'http': 'http://127.0.0.1:7897',
        'https': 'http://127.0.0.1:7897',  # 如果使用相同的代理
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0',
    }
    url = "https://free-proxy-list.net/"
    logger.info("开始爬取"+url)
    response = requests.get(url,headers=headers,proxies=proxies)
    if response.status_code == 200:
        ip_port_pattern = re.compile(r"""(?i)\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?):\d{1,5}""")
        ip_proxy = ip_port_pattern.findall(response.text)
        logger.success("爬取成功")
        return ip_proxy
    else:
        logger.error("爬取失败")