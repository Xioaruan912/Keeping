#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
轮询 roster → inventory，当 “最低价 == TARGET_PRICE” 且 “库存 ≤ TARGET_COUNT” 时提醒一次
"""

import requests, time, sys, re
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
}

TARGET_PRICE  = 174_500      # 目标价格
TARGET_COUNT  = 16           # 目标库存张数（≤ 16）
POLL_INTERVAL = 30           # 秒
last_price    = None         # 上一次最低价

def fetch_min_inventory_price():
    """
    返回 (最低价, 对应库存 int)；若 inventory 为空/解析失败返回 (None, None)
    """
    try:
        r = requests.get(URL, params=PARAMS, headers=HEADERS, timeout=10)
        r.raise_for_status()
        inventory = r.json()["data"]["inventory"]
        if not inventory:
            return None, None

        min_item  = min(inventory, key=lambda x: int(x["price"]))
        min_price = int(min_item["price"])

        # count 可能带 '<' 或 '%'，只取数字
        count_str = min_item["count"]
        count_int = int("".join(re.findall(r"\d+", count_str))) if re.search(r"\d+", count_str) else 0
        return min_price, count_int
    except Exception as e:
        print(datetime.now(), "请求失败:", e, file=sys.stderr)
        return None, None

def notify(price: int, count: int):
    print(f"🎉 价格已降至 {price}，库存 {count} 张！时间 {datetime.now()}")

# ------------- 主循环 -------------
if __name__ == "__main__":
    while True:
        price, count = fetch_min_inventory_price()
        print(datetime.now(), f"当前最低价: {price}，库存: {count}")

        if price is None:
            time.sleep(POLL_INTERVAL)
            continue

        # 价格或库存变化才继续判断，避免重复输出
        if price != last_price:
            if price == TARGET_PRICE and count == TARGET_COUNT:
                notify(price, count)
                break                       # 通知一次后退出；如要持续监控删掉这行
            last_price = price

        time.sleep(POLL_INTERVAL)
