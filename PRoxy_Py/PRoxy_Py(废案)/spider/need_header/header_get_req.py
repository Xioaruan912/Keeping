import random

import requests
from loguru import logger


def need_header_get(url,proxy,headers):
    logger.info("开始访问web:"+ url)
    random_proxy = random.choice(proxy)
    logger.info("随机选取Proxy:"+ random_proxy)
    proxies = {
        "http": f"{random_proxy}",
        "https": f"{random_proxy}"
    }
    logger.debug(proxies)
    response = requests.get(url,headers,proxies=proxies,verify=False)
    return  response.text


