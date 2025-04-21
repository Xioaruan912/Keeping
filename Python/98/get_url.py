import requests
import re
import random
from loguru import logger

def get_target_url():
    baseurl = 'http://sehuatang.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }

    try:
        response = requests.get(baseurl, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"请求失败: {e}")
        return []

    html = response.text
    pattern = r'mappings\.set\("[^"]+",\s*"(https?://[^"]+)"\)'
    matches = re.findall(pattern, html)

    if not matches:
        logger.warning("未匹配到任何URL")
        return []

    logger.info(f"共提取到 {len(matches)} 个地址")

    random_url = random.choice(matches)
    logger.info(f"随机返回的地址: {random_url}")
    return random_url
    