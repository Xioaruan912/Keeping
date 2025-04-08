import json
import time
from flask import Flask, render_template, request
from open_chrome import openChrome
from loguru import logger
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 全局变量存储cookie和最后更新时间
cookie_cache = {
    'value': None,
    'last_update': 0,
    'expire_time': 1800  # 30分钟过期时间（单位：秒）
}

def get_cached_cookie():
    current_time = time.time()
    # 如果cookie不存在或已过期，则重新获取
    if cookie_cache['value'] is None or (current_time - cookie_cache['last_update']) > cookie_cache['expire_time']:
        cookie_cache['value'] = re()
        cookie_cache['last_update'] = current_time
        print("重新获取了cookie")
    else:
        print("使用缓存的cookie")
    return cookie_cache['value']

def get_cookie_string(driver) -> str:

    try:
        # 获取浏览器所有Cookie
        cookies = driver.get_cookies()

        # 拼接有效Cookie
        return "; ".join(
            f"{c['name']}={c['value']}"
            for c in cookies
            if c.get('name') and c.get('value')
        )

    except Exception:
        return ""

def re():
    username = 
    password = 
    driver = openChrome()
    logger.info("开始处理登入逻辑")
    driver.get("https://account.chsi.com.cn/passport/login?entrytype=yzgr&service=https%3A%2F%2Fyz.chsi.com.cn%2Fsytj%2Fj_spring_cas_security_check")
    logger.info("当前导向:" + driver.title)
    driver.find_element(By.XPATH,"""//*[@id="username"]""").send_keys(username)
    driver.find_element(By.XPATH,"""//*[@id="password"]""").send_keys(password)
    driver.find_element(By.XPATH,"""//*[@id="fm1"]/div[4]/input[4]""").click()
    time.sleep(5)
    cookies = get_cookie_string(driver)
    return cookies

def check(driver):
    URL = "https://yz.chsi.com.cn/sytj/tj/fstz.action"
    driver.get(URL)


def get_data():
        # 获取前端传递的专业名称，默认为“网络与信息安全”
    zymc = request.form.get('zymc', '网络与信息安全') if request.method == 'POST' else '网络与信息安全'
    cookie = get_cached_cookie()
    # 调用接口并获取数据
    url = 'https://yz.chsi.com.cn/sytj/stu/sytjqexxcx.action'  # 你实际的接口URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': cookie
    }

    # 这里的分页控制开始
    all_data = []  # 用于存储所有数据
    for start in range(0, 401, 20):  # 从 0 到 200，步长为 20
        payload = {
            'orderBy': '',
            'ssdm': '',
            'dwmc': '',
            'xxfs': '1',  # 使用按页查询
            'zxjh': '0',
            'qers:' : '0',
            'zymc': zymc,  # 这里动态传递专业名称
            'start': str(start),  # 控制分页
            'pageSize': '20'  # 每页 20 条
        }

        response = requests.post(url, headers=headers, data=payload)
        try:
            # 解析响应数据
            data = response.json()

            # 检查 'vos' 字段是否存在并且非空
            vos_data = data.get('msg', {}).get('data', {}).get('vo_list', {}).get('vos', [])

            if not vos_data:  # 如果没有数据，跳出循环
                break

            all_data.extend(vos_data)  # 添加当前页数据到总数据列表

        except ValueError:
            return f"接口返回的内容不是有效的JSON格式：{response.text}", 500
        except KeyError:
            return f"响应数据缺少预期的字段，可能数据格式发生变化。", 500

    # 返回所有数据到前端
    return all_data,zymc