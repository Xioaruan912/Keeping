from spider.need_header.header_get_req import need_header_get
from spider.need_header.header_post_req import need_header_post
from spider.no_headers.get_req import main_get_request
from spider.no_headers.post_req import main_post_request
from spider.spider_site.chech_life import check_proxies
from loguru import logger
from spider.spider_site.free_proxy_list import free_proxy_list

def clean_json_string(json_str: str) -> str:
    # 移除所有空白字符（包括空格、换行符等）
    cleaned = ''.join(json_str.split())
    return cleaned


def main_spider(url,post_data,headers):
    logger.info("开始执行爬虫任务...")
    ip = free_proxy_list()
    usable_proxies = check_proxies(ip, max_workers=15)
    logger.success(f"可用的代理数量: {len(usable_proxies)}")
    logger.success(usable_proxies)
    if headers is None:
        if post_data == None:
            logger.debug("自动带头执行get任务")
            raw = main_get_request(url, usable_proxies)
            return raw
        else:
            logger.debug("自动带头执行post任务")
            raw = main_post_request(url, post_data, usable_proxies)
            return raw
    else:
        if post_data == None:
            logger.debug("不带头执行get任务")
            raw = need_header_get(url, usable_proxies,headers)
            return raw
        else:
            logger.debug("不带头执行post任务")
            raw = need_header_post(url, post_data ,usable_proxies,headers)
            return raw