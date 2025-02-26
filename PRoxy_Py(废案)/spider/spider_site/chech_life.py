import re
from loguru import logger
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

TEST_URL = "https://httpbin.org/ip"
TIMEOUT = 5

# 正则表达式同上
ip_port_pattern = re.compile(
    r'^(\d{1,3}\.){3}\d{1,3}:\d{1,5}$'
)


def is_valid_ip_port(proxy):
    return re.match(ip_port_pattern, proxy) is not None


def check_proxy(proxy):

    proxies = {
        "http": proxy,
        "https": proxy
    }
    try:
        response = requests.get(TEST_URL, proxies=proxies,timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            return proxy
    except Exception as e:
        # 可以根据需要记录错误日志
        pass
    return None


def check_proxies(proxy_list, max_workers=10):
    logger.info("开始测试代理存活")
    available_proxies = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxy_list if is_valid_ip_port(proxy)}

        for future in as_completed(future_to_proxy):
            result = future.result()
            if result:
                available_proxies.append(result)
    return available_proxies  # 移出循环