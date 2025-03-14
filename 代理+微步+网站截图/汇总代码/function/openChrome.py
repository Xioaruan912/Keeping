import os
import shutil

from loguru import logger
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from function.main_request import main_req_func


#################################### 初始化 Chrome ############################################
def open_Chrome(username, password):
    """
    初始化 Chrome 浏览器并执行登录逻辑。
    :param username: 用户名
    :param password: 密码
    :return: 登录成功后的 WebDriver 对象，失败返回 None
    """
    logger.info("初始化 Chrome")

    # 配置 Chrome 选项
    chrome_options = Options()

    # 反反爬虫设置
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 禁用自动化控制特征
    chrome_options.add_argument("--start-maximized")  # 浏览器窗口最大化

    # 禁用图形界面（可选）
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速

    # 默认配置
    chrome_options.add_experimental_option("detach", True)  # 关键参数，防止浏览器自动关闭
    chrome_options.add_argument("--log-level=INFO")  # 设置日志级别为 INFO
    chrome_options.add_argument("--disable-web-security")  # 禁用 Web 安全
    chrome_options.add_argument("--disable-extensions")  # 禁用扩展
    chrome_options.add_argument("--disable-notifications")  # 禁用通知
    chrome_options.add_argument("--disable-infobars")  # 隐藏"Chrome正受到自动测试软件的控制"的通知
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 防止显示自动化信息
    chrome_options.add_experimental_option('useAutomationExtension', False)  # 不使用自动化扩展

    # 设置自定义 User-Agent
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    ######################################### 处理 ChromeDriver ##########################################
    chrome_driver_path = r"./Chorme_driver/"  # ChromeDriver 保存路径
    chrome_driver = os.path.join(chrome_driver_path, 'chromedriver.exe')  # ChromeDriver 完整路径

    # 如果 ChromeDriver 不存在，则下载并保存
    if not os.path.exists(chrome_driver):
        logger.info("下载 Chromedriver")
        if not os.path.exists(chrome_driver_path):  # 如果目录不存在则创建
            os.mkdir(chrome_driver_path)
        driver_path = ChromeDriverManager().install()  # 下载 ChromeDriver
        logger.info("driver_path : " + driver_path)
        shutil.copy(driver_path, chrome_driver)  # 复制到指定路径
        logger.info("下载至:" + chrome_driver + "成功")

    # 初始化 ChromeDriver 服务
    service = Service(chrome_driver)  # 自动配置 Chrome 爬虫环境
    driver = webdriver.Chrome(service=service, options=chrome_options)  # 使用服务启动 Chrome
    logger.success("初始化成功")

    ########################################## 开始请求 #########################################
    # 调用登录逻辑
    driver = main_req_func(driver, username, password)
    if driver is None:  # 如果登录失败
        return None
    logger.success("账号初始化成功")
    return driver