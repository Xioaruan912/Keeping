import json
import time

from open_chrome import openChrome
from loguru import logger
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_cookie_string(driver) -> str:
    """
    直接返回可用的Cookie字符串
    格式示例: "session_id=abc123; token=xyz456"

    参数:
        driver: 已经完成登录的WebDriver实例

    返回:
        可直接用于请求头的Cookie字符串
        如果获取失败返回空字符串""
    """
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
    print(cookies)
    return cookies

