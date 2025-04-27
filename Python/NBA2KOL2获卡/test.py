'''
作者: Xioaruan912 xioaruan@gmail.com
最后编辑人员: Xioaruan912 xioaruan@gmail.com
文件作用介绍: 

'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
from datetime import datetime

URL = "https://nba2k2app.game.qq.com/game/trade/roster"
PARAMS = {
    "page": 1,
    "openid": "759EEBC11E3E8641DA223E9FA937CCFF",
    "access_token": "Token",
    "playerId": 4222,
}

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (iPhone; CPU iPhone OS 18_4_1 like Mac OS X) "
                   "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 "
                   "NBA2KOL2HelperI/2.1.0(1.608)"),
    "Accept": "*/*",
    "Content-Type": "application/json;charset=utf-8",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}

def fetch_min_inventory_price():
    """
    返回 (最低价, count) 元组；inventory 为空或字段缺失时返回 None。
    """
    try:
        r = requests.get(URL, params=PARAMS, headers=HEADERS, timeout=10)
        r.raise_for_status()
        inventory = r.json()["data"]["inventory"]

        # 把 price 转成 int 后排序，取最小项
        min_item = min(inventory, key=lambda x: int(x["price"]))
        min_price = int(min_item["price"])
        count     = min_item["count"]           # 原接口给的是字符串

        return min_price, count
    except Exception as e:
        print(datetime.now(), "请求失败:", e, file=sys.stderr)
        return None

if __name__ == "__main__":
    result = fetch_min_inventory_price()
    if result is None:
        print("未获取到价格信息。")
    else:
        price, cnt = result
        print(f"获取到 最低价: {price} \n卡量: {cnt}")
