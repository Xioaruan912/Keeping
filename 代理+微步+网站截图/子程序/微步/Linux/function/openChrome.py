import os.path
import shutil

from loguru import logger
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from function.main_request import main_req_func


#check linux 环境
def env_check():
    if shutil.which("google-chrome-stable") is None:
        logger.info("LINUX 环境配置启动")
        try:
            os.system("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
            os.system("sudo dpkg -i google-chrome-stable_current_amd64.deb")
            os.system("sudo apt-get install -f -y")
            os.system("clear")
            logger.success("执行结束，requestments.txt")
        except:
            logger.error("错误，自检查环境")
# 代理设置 默认关闭
def proxy(chrome_options=None):
    logger.info("代理设置:")
    switch1 = input("是否需要开启代理: 1.Yes 2.No\n")
    if switch1 == '1':
        logger.info("开启代理设置，确保代理设置正确")
        proxy_host = "代理IP地址"
        proxy_port = "端口号"
        proxy_username = "用户名"
        proxy_password = "密码"
        proxy = f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"
        chrome_options.add_argument(f"--proxy-server={proxy}")  # 设置代理IP
    else:
        logger.info("取消设置代理")


#处理验证码图像

def openChrome(username,password):

    env_check()
    logger.info("初始化Chrome")
    chrome_options = Options()
    # proxy(chrome_options=chrome_options)   #代理配置 默认禁用

    #反反爬虫
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")  # 浏览器窗口最大化

    #禁用图形界面
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")  # 设置user-agent

    #处理 chromedriver

    chrome_driver_path = r"""./Chorme_driver/"""
    chrome_driver = chrome_driver_path + 'chromedriver'
    # chrome_driver = os.path.join(chrome_driver_path, 'chromedriver')  # Linux 下的文件名
    if not os.path.exists(chrome_driver):
        if not os.path.exists(chrome_driver_path):
            logger.info("下载Chromedriver")
            os.mkdir(chrome_driver_path)
            os.system("chmod 777 " + chrome_driver_path)
        driver_path = ChromeDriverManager().install()
        logger.info("driver_path : " + driver_path)
        shutil.copy(driver_path, chrome_driver)
        logger.info("下载至:" + chrome_driver + "成功")
    service = Service(chrome_driver)   #自动配置Chrome爬虫环境 运用在第一次运行的电脑使用
    driver = webdriver.Chrome(options=chrome_options,service=service)  #service = service 上面的取消后要加入该配置
    logger.success("初始化成功")
    driver = main_req_func(driver,username,password)
    logger.success("账号初始化成功")
    return driver

