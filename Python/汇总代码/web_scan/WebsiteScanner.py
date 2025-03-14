import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from pyzbar.pyzbar import decode
import io
from loguru import logger
import urllib3
import time

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebsiteScanner:
    def __init__(self, base_url):
        """
        初始化网站扫描器
        :param base_url: 要扫描的网站基础URL
        """
        self.base_url = base_url  # 基础URL
        self.visited_urls = set()  # 已访问的URL集合
        self.qr_results = set()  # 二维码解码结果集合
        self.download_links = set()  # 下载链接集合
        self.image_links = set()  # 图片链接集合
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }  # 请求头
        self.pages_scanned = 0  # 已扫描的页面数
        self.images_processed = 0  # 已处理的图片数
        self.start_time = None  # 扫描开始时间

    def scan_qr_code(self, image_data):
        """
        扫描图片中的二维码
        :param image_data: 图片的二进制数据
        :return: 二维码解码结果列表
        """
        try:
            image = Image.open(io.BytesIO(image_data))  # 打开图片
            decoded_objects = decode(image)  # 解码二维码
            qr_data = [obj.data.decode('utf-8') for obj in decoded_objects]  # 获取解码结果
            if qr_data:
                logger.info(f"发现二维码！解码结果: {qr_data}")
            return qr_data
        except Exception as e:
            logger.error(f"二维码扫描错误: {str(e)}")
            return []

    def find_download_links(self, soup):
        """
        查找页面中的下载链接
        :param soup: BeautifulSoup对象
        """
        download_extensions = [
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.rar', '.7z', '.tar', '.gz', '.exe', '.apk'
        ]  # 下载文件扩展名列表

        new_downloads = 0  # 新发现的下载链接数
        for link in soup.find_all('a', href=True):  # 查找所有链接
            href = link['href']
            full_url = urljoin(self.base_url, href)  # 拼接完整URL

            if any(href.lower().endswith(ext) for ext in download_extensions):  # 判断是否为下载链接
                if full_url not in self.download_links:  # 如果链接未记录
                    self.download_links.add(full_url)  # 添加到下载链接集合
                    new_downloads += 1
                    logger.info(f"发现新下载链接: {full_url}")

        if new_downloads > 0:
            logger.info(f"在当前页面发现 {new_downloads} 个新的下载链接")

    def process_images(self, soup):
        """
        处理页面中的图片
        :param soup: BeautifulSoup对象
        """
        for img in soup.find_all('img', src=True):  # 查找所有图片
            img_url = urljoin(self.base_url, img['src'])  # 拼接完整图片URL
            self.image_links.add(img_url)  # 添加到图片链接集合
            try:
                response = requests.get(img_url, headers=self.headers, verify=False)  # 请求图片
                if response.status_code == 200:  # 如果请求成功
                    self.images_processed += 1
                    logger.debug(f"已处理图片: {img_url}")

                    qr_data = self.scan_qr_code(response.content)  # 扫描二维码
                    if qr_data:
                        self.qr_results.update(qr_data)  # 更新二维码结果集合
            except Exception as e:
                logger.error(f"处理图片错误 {img_url}: {str(e)}")

    def crawl_page(self):
        """
        爬取页面内容
        """
        if self.base_url in self.visited_urls:  # 如果URL已访问过
            return

        self.visited_urls.add(self.base_url)  # 添加到已访问URL集合
        self.pages_scanned += 1  # 增加已扫描页面数
        logger.info(f"\n正在扫描第 {self.pages_scanned} 个页面: {self.base_url}")

        try:
            response = requests.get(self.base_url, headers=self.headers, verify=False)  # 请求页面
            if response.status_code == 200:  # 如果请求成功
                soup = BeautifulSoup(response.text, 'html.parser')  # 解析页面内容

                self.process_images(soup)  # 处理图片
                self.find_download_links(soup)  # 查找下载链接

        except Exception as e:
            logger.error(f"爬取页面错误 {self.base_url}: {str(e)}")

    def scan_website(self):
        """
        扫描网站并返回结果
        :return: 扫描结果字典
        """
        self.start_time = time.time()  # 记录开始时间
        logger.info(f"开始扫描网站: {self.base_url}")
        logger.info("=" * 50)

        self.crawl_page()  # 爬取页面

        duration = time.time() - self.start_time  # 计算扫描耗时
        logger.info("扫描完成！统计信息：")
        logger.info(f"总耗时: {duration:.2f} 秒")
        logger.info(f"扫描页面数: {self.pages_scanned}")
        logger.info(f"处理图片数: {self.images_processed}")
        logger.info(f"发现二维码数: {len(self.qr_results)}")
        logger.info(f"发现下载链接数: {len(self.download_links)}")

        return {
            'statistics': {
                'total_time_seconds': duration,
                'pages_scanned': self.pages_scanned,
                'images_processed': self.images_processed,
                'qr_codes_found': len(self.qr_results),
                'download_links_found': len(self.download_links)
            },
            'qr_codes': list(self.qr_results),
            'download_links': list(self.download_links),
            'image_links': sorted(list(self.image_links)),
        }