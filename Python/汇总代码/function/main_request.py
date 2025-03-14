import os
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from loguru import logger
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from function.Cvcheck import img_attack


############################################### 拖拽验证码处理 ###################################
def deal_img(driver, qk_xpath, hk_xpath):
    """
    处理拖拽验证码，下载缺口图片和滑块图片。
    :param driver: Selenium WebDriver 对象
    :param qk_xpath: 缺口图片的 XPath
    :param hk_xpath: 滑块图片的 XPath
    :return: 缺口图片和滑块图片的本地路径
    """
    save_dir = "img"  # 图片保存目录
    if not os.path.exists(save_dir):  # 如果目录不存在则创建
        os.mkdir(save_dir)

    # 获取缺口图片元素
    qk_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, qk_xpath))
    )
    driver.execute_script("arguments[0].scrollIntoView();", qk_element)  # 滚动到元素位置
    WebDriverWait(driver, 5).until(EC.visibility_of(qk_element))  # 确保元素可见
    qk_url = qk_element.get_attribute("outerHTML")[79:-16]  # 提取图片 URL

    # 获取滑块图片元素
    hk_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, hk_xpath))
    )
    driver.execute_script("arguments[0].scrollIntoView();", hk_element)  # 滚动到元素位置
    WebDriverWait(driver, 5).until(EC.visibility_of(hk_element))  # 确保元素可见
    hk_url = hk_element.get_attribute("outerHTML")[91:-16]  # 提取图片 URL

    # 下载图片的函数
    def download_image(url, filename):
        """
        下载图片并保存到本地。
        :param url: 图片的 URL
        :param filename: 保存的文件名
        """
        response = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

    # 生成随机文件名
    num = random.randint(1, 9999)
    filename_hk = os.path.join(save_dir, f"{num}_hk.png")
    filename_qk = os.path.join(save_dir, f"{num}_qk.png")

    # 使用多线程下载图片
    with ThreadPoolExecutor() as executor:
        executor.submit(download_image, hk_url, filename_hk)
        executor.submit(download_image, qk_url, filename_qk)

    return filename_qk, filename_hk

###################################  主要请求逻辑 #################################################
def main_req_func(driver, username, password):
    """
    处理登录逻辑，包括输入账号密码和绕过验证码。
    :param driver: Selenium WebDriver 对象
    :param username: 用户名
    :param password: 密码
    :return: 登录成功后的 WebDriver 对象，失败返回 None
    """
    logger.info("开始处理登入逻辑")
    driver.get("https://x.threatbook.com/v5/vul/keyword/search?params=%7B%22riskLevel%22%3A%22High%22%7D")
    logger.info("当前导向:" + driver.title)

    # 账号密码登入流程
    driver.find_element(By.XPATH, """//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/div/div[3]/div[2]""").click()
    driver.find_element(By.XPATH, """//*[@id="phoneOrEmail"]""").send_keys(username)
    logger.success("账号输入成功")
    driver.find_element(By.XPATH, """//*[@id="password"]""").send_keys(password)
    logger.success("密码输入成功")
    driver.find_element(By.XPATH,"""//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/div/div[4]/div/label/span""").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"""//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/div/div[4]/form/div[3]/div/input""").click()
    logger.info("开始绕过滑块验证码")
    check_num = True
    attempt = 0
    max_attempts = 5
    while check_num and attempt < max_attempts:
        attempt += 1
        time.sleep(2)  # 暂停以等待页面加载

        try:
            # 获取验证码框
            hk_box = driver.find_element(By.XPATH,
                                         """/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]""")
            qk_xpath = "/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]"
            hk_xpath = "/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]"

            # 处理图片
            qk, hk = deal_img(driver, qk_xpath, hk_xpath)
            img_attack(qk, hk, driver, hk_box)
            time.sleep(5)
            # 检查页面标题
            if driver.title != "ThreatBook 用户登录":
                print(f"当前页面标题: {driver.title}")
                logger.success("登入验证码绕过成功")
                return driver
            else:
                try:
                    # 等待错误信息出现
                    error_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        """//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/div/div[4]/form/div[3]/div/div[2]"""))
                    ).text
                    if "手机号与密码不匹配" in error_element:
                        logger.error("账号密码错误")
                        return None  # 返回None表示登录失败
                    else:
                        logger.info("重试拖拽")
                        continue
                except (NoSuchElementException, TimeoutException):
                    logger.warning("未找到错误信息，继续重试拖拽")
                    continue
        except Exception as e:
            logger.error(f"处理过程中发生错误: {str(e)}")
            if attempt >= max_attempts:
                logger.error(f"已达到最大尝试次数({max_attempts})，登录失败")
                return None
    logger.error("登录失败，已达到最大尝试次数")
    return None

################################## 查询逻辑 ################################################
def search_req(driver, string_search):
    """
    执行搜索操作。
    :param driver: Selenium WebDriver 对象
    :param string_search: 搜索关键词
    """
    logger.info("开始执行搜索:" + string_search)
    search_box = driver.find_element(By.XPATH,
                                     """//*[@id="app"]/div[1]/header/div[2]/div/div[1]/div/div/div[1]/div[1]/div[2]/textarea""")
    search_box.click()
    search_box.send_keys(string_search)
    driver.find_element(By.XPATH,
                        """//*[@id="app"]/div[1]/header/div[2]/div/div[1]/div/div/div[1]/div[1]/div[3]/span[2]""").click()
    logger.success("搜索 -" + string_search + "结束")

############################### 反爬虫逻辑 ###############################################
def bypass(driver, xpath, qk_xpath, hk_xpath):
    """
    绕过反爬虫机制，处理拖拽验证码。
    :param driver: Selenium WebDriver 对象
    :param xpath: 滑块的 XPath
    :param qk_xpath: 缺口图片的 XPath
    :param hk_xpath: 滑块图片的 XPath
    """
    try:
        check_box = driver.find_element(By.XPATH, """//*[@id="app"]/div[1]/div[1]/div/div/div[1]/div/div[1]""").text
        if check_box == "不是机器人？请完成验证继续使用X情报社区。":
            logger.info("识别到反爬虫机制")
            time.sleep(1)
        else:
            logger.success("不存在反爬虫机制")
            return
    except:
        logger.success("不存在反爬虫机制")
        return

    driver.find_element(By.XPATH, """//*[@id="captcha-zone"]/div/div/div[1]""").click()
    check_num = True
    while check_num:
        hk_box = driver.find_element(By.XPATH, xpath)
        qk, hk = deal_img(driver, qk_xpath, hk_xpath)
        img_attack(qk, hk, driver, hk_box)

        try:
            check_text = driver.find_element(By.XPATH, """/html/body/div[5]/div[2]/div/div[1]/div[1]/div[1]""").text
            continue
        except:
            break

    logger.success("ByPass 反爬虫")

################################ 获取token逻辑 ###########################################
def get_auth(driver):
    """
    从请求头中提取 CSRF Token 和 Cookie。
    :param driver: Selenium WebDriver 对象
    :return: x-csrf-token, xx-csrf, cookie
    """
    for request in driver.requests:
        if request.path == "/v5/node/message/count":
            result = request.headers

    pattern = re.compile(r'^(x-csrf-token|xx-csrf|cookie):\s*(.+)$', re.MULTILINE)

    results = {}
    for match in pattern.finditer(str(result)):
        key = match.group(1).lower()
        value = match.group(2).strip()
        results[key] = value

    x_csrf_token = results.get('x-csrf-token', '未找到')
    xx_csrf = results.get('xx-csrf', '未找到')
    cookie = results.get('cookie', '未找到')
    return x_csrf_token, xx_csrf, cookie