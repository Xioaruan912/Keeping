import shutil
import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger

def open_chrome():
    chrome_options = webdriver.ChromeOptions()

    # 反反爬虫配置
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # 日志等级与 UA 设置
    chrome_options.add_argument("--log-level=INFO")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

    # Headless 模式与其他配置
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Linux 无 DISPLAY 时强制 headless
    if os.environ.get("DISPLAY", "") == "":
        logger.info("未检测到图形环境，启用 headless 模式")
        chrome_options.add_argument("--headless=new")
    else:
        chrome_options.add_argument("--start-maximized")


    # 处理 chromedriver 路径与下载
    chrome_driver_path = "./Chorme_driver/"
    system_platform = platform.system().lower()
    is_windows = system_platform == "windows"
    driver_name = "chromedriver.exe" if is_windows else "chromedriver"
    chrome_driver = os.path.join(chrome_driver_path, driver_name)

    if not os.path.exists(chrome_driver):
        logger.info("未检测到 Chromedriver，尝试下载")
        os.makedirs(chrome_driver_path, exist_ok=True)
        driver_path = ChromeDriverManager().install()
        logger.info("driver_path : " + driver_path)
        shutil.copy(driver_path, chrome_driver)
        logger.info("下载至: " + chrome_driver + " 成功")

    # 启动浏览器
    service = Service(chrome_driver)
    driver = webdriver.Chrome(options=chrome_options, service=service)
    return driver
