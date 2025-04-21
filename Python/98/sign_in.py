
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from loguru import logger
def sign_in(driver,url):
    logger.info("开始处理签到")
    sign_url = url+"plugin.php?id=dd_sign"
    driver.get(sign_url)
    sign = driver.find_element(By.XPATH,"""//*[@id="wp"]/div[2]/div[1]/div[1]/a""").text
    if sign == "今日已签到":
        logger.success("当前账号已经签到")
        return sign
    try:
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='wp']/div[2]/div[1]/div[1]/a"))
    ).click()
        text_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, """//div[@class='rfm']//table/tbody/tr/td"""))
        )
        text = text_element.text
        logger.info("开始处理签到验证")
        equation = text.replace("换一个", "").strip()
        cleaned_text = equation.replace("=", "").replace("?", "").strip()
        parts = cleaned_text.split()
        if len(parts) == 3:
            num1 = int(parts[0])
            operator = parts[1]
            num2 = int(parts[2])

            # 根据运算符进行计算
            if operator == "+":
                result = num1 + num2
            elif operator == "-":
                result = num1 - num2
            elif operator == "*":
                result = num1 * num2
            elif operator == "/":
                result = num1 / num2
            else:
                raise ValueError("未知运算符")
        driver.find_element(By.NAME, "secanswer").send_keys(str(result))
        driver.find_element(By.NAME, "signsubmit").click()
        logger.success("签到成功")
        return "签到成功"
    except:
        return "系统繁忙"

    