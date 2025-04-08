from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import shutil
import logging
import platform

logger = logging.getLogger(__name__)


def openChrome():
    """Mac 优化的 Chrome 启动函数"""
    try:
        logger.info("正在初始化 Chrome（Mac 优化版）")
        chrome_options = Options()

        # 反爬虫配置
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # Mac 专属配置
        if platform.system() == 'Darwin':
            chrome_options.add_argument("--kiosk")  # Mac 全屏模式
            chrome_options.add_argument("--use-fake-ui-for-media-stream")  # 自动授权媒体设备
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        else:
            chrome_options.add_argument("--start-maximized")
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

        chrome_options.add_argument(f"--user-agent={user_agent}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Disable GUI (uncomment if needed)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        # 驱动路径处理（自动创建~/Chrome_driver目录）
        chrome_driver_dir = os.path.expanduser("~/Chrome_driver")
        chrome_driver_path = os.path.join(chrome_driver_dir, "chromedriver")

        if not os.path.exists(chrome_driver_path):
            os.makedirs(chrome_driver_dir, exist_ok=True)
            logger.info("正在自动下载 Chromedriver...")
            driver_path = ChromeDriverManager().install()
            shutil.copy(driver_path, chrome_driver_path)
            os.chmod(chrome_driver_path, 0o755)  # Mac 必须赋予可执行权限
            logger.info(f"驱动已安装到: {chrome_driver_path}")

        # 启动 Chrome
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(options=chrome_options, service=service)
        logger.info("Chrome 启动成功")
        return driver

    except Exception as e:
        logger.error(f"Chrome 启动失败: {str(e)}")
        raise