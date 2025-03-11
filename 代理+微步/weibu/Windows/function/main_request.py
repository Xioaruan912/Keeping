import os
import random
import re
import time

import requests
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from function.Cvcheck import img_attack


def deal_img(driver,qk_xpath,hk_xpath):
    save_dir = "img"
    if not os.path.exists("./" + save_dir):
        os.mkdir("./" + save_dir)
    time.sleep(1)
    # 缺口
    qk_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"{qk_xpath}"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", qk_element)  # 滚动到元素位置
    WebDriverWait(driver, 5).until(EC.visibility_of(qk_element))  # 确保元素可见

    qk_url = qk_element.get_attribute("outerHTML")[79:-16]

    # 滑块
    hk_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"{hk_xpath}"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", hk_element)  # 滚动到元素位置
    WebDriverWait(driver, 5).until(EC.visibility_of(hk_element))  # 确保元素可见
    hk_box = hk_element.get_attribute("src")
    hk_url = hk_element.get_attribute("outerHTML")[91:-16]
    response_hk = requests.get(hk_url, stream=True)
    response_qk = requests.get(qk_url, stream=True)
    rd = random.Random()
    num = rd.randint(1, 9999)
    filename_hk = f"{num}_hk.png"
    file_path_hk = os.path.join(save_dir, filename_hk)
    with open(file_path_hk, 'wb') as f:
        for chunk in response_hk.iter_content(1024):
            f.write(chunk)
    filename_qk = f"{num}_qk.png"
    file_path_qk = os.path.join(save_dir, filename_qk)
    with open(file_path_qk, 'wb') as f:
        for chunk in response_qk.iter_content(1024):
            f.write(chunk)
    return file_path_qk, file_path_hk
def main_req_func(driver,username,password):
    logger.info("开始处理登入逻辑")
    driver.get("https://x.threatbook.com/v5/vul/keyword/search?params=%7B%22riskLevel%22%3A%22High%22%7D")
    logger.info("当前导向:"+driver.title)
    # 账号密码登入流程
    driver.find_element(By.XPATH, """//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/div/div[3]/div[2]""").click()
    driver.find_element(By.XPATH, """//*[@id="phoneOrEmail"]""").send_keys(username)
    logger.success(f"账号输入成功")
    driver.find_element(By.XPATH, """//*[@id="password"]""").send_keys(password)
    logger.success(f"密码输入成功")
    driver.find_element(By.XPATH,
                        """//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/div/div[4]/div/label/span""").click()
    time.sleep(2)  # 等待登入
    driver.find_element(By.XPATH,
                        """//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/div/div[4]/form/div[3]/div/input""").click()
    logger.info("开始绕过滑块验证码")
    check_num = True
    while(check_num):
        time.sleep(2)
        hk_box = driver.find_element(By.XPATH,"""/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]""")
        qk_xpath = "/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]"
        hk_xpath = "/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]"
        qk, hk = deal_img(driver,qk_xpath,hk_xpath)
        img_attack(qk, hk, driver, hk_box)
        time.sleep(4)
        if(driver.title != "ThreatBook 用户登录"):
            check_num = False
            logger.success("登入验证码绕过成功")
        else:
            continue
        break
    time.sleep(1)
    return driver

#处理搜索的爬虫
def search_req(driver,string_search):
    logger.info("开始执行搜索:" + string_search)
    search_box = driver.find_element(By.XPATH,"""//*[@id="app"]/div[1]/header/div[2]/div/div[1]/div/div/div[1]/div[1]/div[2]/textarea""")
    search_box.click()
    search_box.send_keys(string_search)
    driver.find_element(By.XPATH,"""//*[@id="app"]/div[1]/header/div[2]/div/div[1]/div/div/div[1]/div[1]/div[3]/span[2]""").click()
    logger.success("搜索 -" + string_search + "结束")


# 处理反爬的代码
def bypass(driver,xpath,qk_xpath,hk_xpath):
    try:
        check_box = driver.find_element(By.XPATH,"""//*[@id="app"]/div[1]/div[1]/div/div/div[1]/div/div[1]""").text
        if (check_box == "不是机器人？请完成验证继续使用X情报社区。"):
            logger.info("识别到反爬虫机制")
            time.sleep(1)
        else:
            logger.success("不存在反爬虫机制")
            return
    except:
        logger.success("不存在反爬虫机制")
        return
        time.sleep(3)
    driver.find_element(By.XPATH,"""//*[@id="captcha-zone"]/div/div/div[1]""").click()
    time.sleep(1)
    check_num = True
    while(check_num):
        hk_box = driver.find_element(By.XPATH,xpath)
        qk, hk = deal_img(driver,qk_xpath,hk_xpath)
        img_attack(qk, hk, driver, hk_box)
        time.sleep(3)
        try:
            check_text = driver.find_element(By.XPATH,"""/html/body/div[5]/div[2]/div/div[1]/div[1]/div[1]""").text
            continue
        except:
            break
    logger.success("ByPass 反爬虫")
    time.sleep(3)

def get_auth(driver):
    for request in driver.requests:
        if request.path == "/v5/node/message/count":
            result = request.headers

    pattern = re.compile(r'^(x-csrf-token|xx-csrf|cookie):\s*(.+)$', re.MULTILINE)

    # 提取目标字段的值
    results = {}
    for match in pattern.finditer(str(result)):
        key = match.group(1).lower()  # 统一转为小写方便后续处理
        value = match.group(2).strip()
        results[key] = value
    x_csrf_token = result.get('x-csrf-token', '未找到')
    xx_csrf = result.get('xx-csrf', '未找到')
    cookie = result.get('cookie', '未找到')
    return x_csrf_token,xx_csrf,cookie