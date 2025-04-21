
import time
from selenium.webdriver.common.by import By
import random
from selenium.common.exceptions import NoSuchElementException
import random
from loguru  import logger
def pinlun(driver, url, acc):
    logger.info("开始评论功能")
    random_part = random.randint(271979, 371979)
    sign_url = f"{url}forum.php?mod=viewthread&tid={random_part}&extra=page%3D2"

    while True:
        
        driver.get(sign_url)
        logger.info(f"当前web为：【{driver.title}】")
        time.sleep(3)
        try:
            # 尝试点击并填写评论
            comment_box = driver.find_element(By.XPATH, """//*[@id="fastpostmessage"]""")
            comment_box.click()
            comment_box.send_keys(acc.pinlun)
            time.sleep(2)
            driver.find_element(By.XPATH, """//*[@id="fastpostsubmit"]""").click()
            random_part = random.randint(15, 20) 
            logger.success("评论成功,开始等待评论过渡期")    
            time.sleep(random_part)    

            break
        except NoSuchElementException:
            # 如果没有找到元素，重新生成一个新的 sign_url
            random_part = random.randint(271979, 273979)
            sign_url = f"{url}forum.php?mod=viewthread&tid={random_part}&extra=page%3D2"
            logger.info("查找失败 重新查找评论web")
