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
        self.base_url = base_url
        self.visited_urls = set()
        self.qr_results = set()
        self.download_links = set()
        self.image_links = set()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.pages_scanned = 0
        self.images_processed = 0
        self.start_time = None

    def scan_qr_code(self, image_data):
        """扫描图片中的二维码"""
        try:
            image = Image.open(io.BytesIO(image_data))
            decoded_objects = decode(image)
            qr_data = [obj.data.decode('utf-8') for obj in decoded_objects]
            if qr_data:
                logger.info(f"发现二维码！解码结果: {qr_data}")
            return qr_data
        except Exception as e:
            logger.error(f"二维码扫描错误: {str(e)}")
            return []

    def find_download_links(self, soup):
        """查找下载链接"""
        download_extensions = [
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.rar', '.7z', '.tar', '.gz', '.exe', '.apk'
        ]

        new_downloads = 0
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(self.base_url, href)

            if any(href.lower().endswith(ext) for ext in download_extensions):
                if full_url not in self.download_links:
                    self.download_links.add(full_url)
                    new_downloads += 1
                    logger.info(f"发现新下载链接: {full_url}")

        if new_downloads > 0:
            logger.info(f"在当前页面发现 {new_downloads} 个新的下载链接")

    def process_images(self, soup):
        """处理页面中的图片"""
        for img in soup.find_all('img', src=True):
            img_url = urljoin(self.base_url, img['src'])
            self.image_links.add(img_url)
            try:
                response = requests.get(img_url, headers=self.headers, verify=False)
                if response.status_code == 200:
                    self.images_processed += 1
                    logger.debug(f"已处理图片: {img_url}")

                    qr_data = self.scan_qr_code(response.content)
                    if qr_data:
                        self.qr_results.update(qr_data)
            except Exception as e:
                logger.error(f"处理图片错误 {img_url}: {str(e)}")

    def crawl_page(self):
        """爬取指定页面"""
        if self.base_url in self.visited_urls:
            return

        self.visited_urls.add(self.base_url)
        self.pages_scanned += 1
        logger.info(f"\n正在扫描第 {self.pages_scanned} 个页面: {self.base_url}")

        try:
            response = requests.get(self.base_url, headers=self.headers, verify=False)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                self.process_images(soup)
                self.find_download_links(soup)

        except Exception as e:
            logger.error(f"爬取页面错误 {self.base_url}: {str(e)}")

    def scan_website(self):
        """开始扫描网站"""
        self.start_time = time.time()
        logger.info(f"开始扫描网站: {self.base_url}")
        logger.info("=" * 50)

        self.crawl_page()

        duration = time.time() - self.start_time
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