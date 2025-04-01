import random
from loguru import logger
import requests
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def need_header_post(url, post_data, proxy, headers_str):
    logger.info("开始访问web:" + url)
    random_proxy = random.choice(proxy)
    logger.info("随机选取Proxy:" + random_proxy)
    # proxies = {
    #     "http": f"http://{random_proxy}",
    #     "https": f"http://{random_proxy}"
    # }

    proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
    # 处理请求头
    headers = {}
    try:
        pairs = headers_str.strip('"').split('","')
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':', 1)
                key = key.strip().strip('"')
                value = value.strip().strip('"')
                headers[key] = value
    except Exception as e:
        pass


    logger.info("开始发送请求")
    # 发送请求
    response = requests.post(
        url,
        proxies=proxies,
        data=post_data,
        headers=headers,
        verify=False,
        allow_redirects=True  # 允许重定向
    )
    logger.info(response.text)
    return response.text

