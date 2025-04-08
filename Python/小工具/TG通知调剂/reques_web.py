import os
import time
import json
from selenium.webdriver.common.by import By
import requests
from loguru import logger
from open_chrome import openChrome  # Assuming this is your custom module

# Cookie文件路径
COOKIE_FILE = "cookie_cache.json"
# Cookie有效期（15分钟）
COOKIE_EXPIRE_TIME = 900  # 15分钟 = 900秒


def save_cookie_to_file(cookie_value):
    """保存Cookie到文件"""
    cookie_data = {
        'value': cookie_value,
        'last_update': time.time()
    }
    try:
        with open(COOKIE_FILE, 'w') as f:
            json.dump(cookie_data, f)
        logger.info("Cookie已保存到文件")
    except Exception as e:
        logger.error(f"保存Cookie到文件失败: {e}")


def load_cookie_from_file():
    """从文件加载Cookie"""
    if not os.path.exists(COOKIE_FILE):
        return None, 0

    try:
        with open(COOKIE_FILE, 'r') as f:
            cookie_data = json.load(f)
        return cookie_data.get('value'), cookie_data.get('last_update', 0)
    except Exception as e:
        logger.error(f"从文件加载Cookie失败: {e}")
        return None, 0


def get_cached_cookie():
    """获取缓存的Cookie，必要时重新登录获取"""
    # 先从文件加载
    cookie_value, last_update = load_cookie_from_file()

    current_time = time.time()
    # 如果Cookie不存在或已过期，则重新获取
    if cookie_value is None or (current_time - last_update) > COOKIE_EXPIRE_TIME:
        logger.info("Cookie已过期或不存在，重新获取...")
        new_cookie = login_and_get_cookie()
        if new_cookie:
            save_cookie_to_file(new_cookie)
            return new_cookie
        return None
    else:
        logger.info("使用文件中的有效Cookie")
        return cookie_value


def login_and_get_cookie():
    """登录并获取新Cookie"""
    username = 
    password = 
    driver = openChrome()
    logger.info("开始处理登入逻辑")
    driver.get(
        "https://account.chsi.com.cn/passport/login?entrytype=yzgr&service=https%3A%2F%2Fyz.chsi.com.cn%2Fsytj%2Fj_spring_cas_security_check")
    logger.info(f"当前导向: {driver.title}")

    try:
        driver.find_element(By.XPATH, """//*[@id="username"]""").send_keys(username)
        driver.find_element(By.XPATH, """//*[@id="password"]""").send_keys(password)
        driver.find_element(By.XPATH, """//*[@id="fm1"]/div[4]/input[4]""").click()
        time.sleep(5)
        cookies = get_cookie_string(driver)
        return cookies
    except Exception as e:
        logger.error(f"登录失败: {e}")
        return ""
    finally:
        driver.quit()


def get_cookie_string(driver) -> str:
    """从浏览器获取Cookie字符串"""
    try:
        cookies = driver.get_cookies()
        return "; ".join(
            f"{c['name']}={c['value']}"
            for c in cookies
            if c.get('name') and c.get('value')
        )
    except Exception as e:
        logger.error(f"获取cookie失败: {e}")
        return ""


def get_data(zymc="网络与信息安全"):
    """获取调剂数据，返回原始数据和专业名称"""
    cookie = get_cached_cookie()
    if not cookie:
        return None, "无法获取有效Cookie"

    url = 'https://yz.chsi.com.cn/sytj/stu/sytjqexxcx.action'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': cookie
    }

    all_data = []
    for start in range(0, 401, 20):  # 从0到400，步长为20
        payload = {
            'orderBy': '',
            'ssdm': '',
            'dwmc': '',
            'xxfs': '1',
            'zxjh': '0',
            'qers:': '0',
            'zymc': zymc,
            'start': str(start),
            'pageSize': '20'
        }

        try:
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()

            data = response.json()
            vos_data = data.get('msg', {}).get('data', {}).get('vo_list', {}).get('vos', [])

            if not vos_data:
                break

            all_data.extend(vos_data)
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {e}")
            return None, f"请求失败: {str(e)}"
        except (ValueError, KeyError) as e:
            logger.error(f"解析响应数据失败: {e}")
            return None, "解析响应数据失败"
    return all_data, zymc