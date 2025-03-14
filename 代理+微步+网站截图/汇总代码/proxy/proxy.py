import random

def rebuild_headers(headers):
    """
    重建请求头，移除不需要的头部字段。
    :param headers: 原始请求头字典
    :return: 过滤后的请求头字典
    """
    # 需要排除的头部字段
    excluded_headers = [
        'content-encoding', 'content-length', 'transfer-encoding',
        'connection', 'host', 'target', 'ip',
    ]
    # 过滤并返回新的请求头
    return {key: value for key, value in headers.items() if key.lower() not in excluded_headers}

def get_random_ua():
    """
    随机生成一个 User-Agent 字符串。
    :return: 随机选择的 User-Agent 字符串
    """
    # 预定义的 User-Agent 列表
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
    ]
    # 随机选择一个 User-Agent
    return random.choice(user_agents)

def add_browser_headers(headers):
    """
    添加浏览器常用的请求头字段。
    :param headers: 原始请求头字典
    :return: 合并后的请求头字典
    """
    # 浏览器常用的请求头字段
    common_headers = {
        'User-Agent': get_random_ua(),  # 随机生成 User-Agent
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',  # 接受的语言
        'Accept-Encoding': 'gzip, deflate, br',  # 接受的编码
        'Connection': 'keep-alive',  # 保持连接
        'Cache-Control': 'max-age=0'  # 缓存控制
    }
    # 合并原始请求头和常用请求头
    merged_headers = common_headers.copy()
    merged_headers.update(headers)
    return merged_headers