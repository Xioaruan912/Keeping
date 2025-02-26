# 网站扫描

## 用法

```
pip install -r requestments.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple/ 
python3 ./main.py
```

 `127.0.0.1:5000` 路由 `scan`

```
curl -X POST http://127.0.0.1:5000/scan \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.example.com"}'
```

```
POST /scan HTTP/1.1
Host: 127.0.0.1:5000
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Type: application/json
Content-Length: 40

{
"url":"https://www.manhuaren.com/"
}
```

结果

```
HTTP/1.1 200 OK
Server: Werkzeug/3.1.3 Python/3.9.13
Date: Wed, 26 Feb 2025 05:34:19 GMT
Content-Type: application/json
Content-Length: 2462
Connection: close

{"statistics":{"total_time_seconds":4.148070573806763,"pages_scanned":1,"images_processed":25,"qr_codes_found":2,"download_links_found":1},"qr_codes":["https://weibo.com/5228599199/profile?topnav=1&wvr=6","http://www.manhuaren.com/download/"],"download_links":["https://teldown.manhuaren.com/android/app/manhuarenjsb_3-7-8-6.apk"],"image_links":["https://css99tel.cdndm5.com/v202411181654/manhuaren/images/gaicp.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/index-top-right-2.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-app-demo-2.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-app-icon-2.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-banner-1.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-banner-2.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-banner-3.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-banner-4.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-banner-5.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-banner-6.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-banner-7.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-banner-a.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-icon-android-2.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-icon-android.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-icon-apple-2.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-icon-apple.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-icon-qq.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-icon-wb.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-mhr-logo.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/down-qrcode-3.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/footer-logo-2.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/indexDownload/weibo.png","https://css99tel.cdndm5.com/v202411181654/manhuaren/images/new/new_manhuaren_logo_2.png"]}

```



## 代码解释

二维码

首先处理图片 然后对图片进行二维码处理 如果处理成功代表是二维码

```python
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
```

使用 `PIL`的 `decode` 扫描二维码内容

```python
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

```

### 文件下载

暴力 查看后缀匹配

```python
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
```

### 返回信息

```python
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
```

