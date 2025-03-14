import logging
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, make_response
from selenium.webdriver.support.ui import WebDriverWait
from picture_function.openChrome import openChrome
from picture_function.picture_get import fix_url_protocol

# ================= 初始化 Flask 应用 =================
app = Flask(__name__)

# ================= 日志配置 =================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# ================= 代理配置逻辑 =================

# ================= 截图接口 =================
@app.route('/api/capture', methods=['POST'])
def capture_website_screenshot():
    """截图指定网页并返回 PNG 图片"""

    try:

        data = request.json
        url = data.get('url')
        proxy = data.get('proxy')

        if not url:
            logger.error("缺少必要参数: url")
            return jsonify({"error": "Missing 'url'"}), 400

        # 补全协议
        fixed_url = fix_url_protocol(url,proxy)
        if not fixed_url:
            return jsonify({"error": "URL 不可访问"}), 400

        # 初始化浏览器
        driver = openChrome(proxy)
        try:
            logger.info(f"访问 URL: {fixed_url}")
            driver.get(fixed_url)
            time.sleep(5)  # 等待页面加载
            driver.set_window_size(1920, 1080)
            screenshot_data = driver.get_screenshot_as_png()

            # 构造响应
            response = make_response(screenshot_data)
            response.headers.set('Content-Type', 'image/png')
            response.headers.set('Content-Disposition', 'attachment', filename='screenshot.png')
            return response
        except Exception as e:
            logger.error(f"截图失败: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            driver.quit()
    except Exception as e:
        logger.error(f"全局异常: {str(e)}")
        return jsonify({"error": "服务器错误"}), 500


@app.route('/api/icon', methods=['POST'])
def extract_icon_elements():
    try:
        data = request.json
        url = data.get('url')
        proxy = data.get('proxy')

        if not url:
            return jsonify({"error": "Missing 'url'"}), 400

        fixed_url = fix_url_protocol(url,proxy)
        if not fixed_url:
            return jsonify({"error": "URL 不可访问"}), 400

        driver = openChrome(proxy)
        try:
            logger.info(f"正在提取图标: {fixed_url}")
            driver.get(fixed_url)
            
            # 等待页面加载完成
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            logger.info("页面加载完成")

            # 解析页面获取图标URL
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            icon_link = soup.find("link", rel=lambda x: x and x in ["icon", "shortcut icon"])
            icon_url = urljoin(fixed_url, icon_link['href']) if icon_link else urljoin(fixed_url, '/favicon.ico')
            logger.info(f"图标地址: {icon_url}")

            # 使用 driver 加载图标
            driver.get(icon_url)
            
            # 等待图标加载完成
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            logger.info("图标加载完成")

            # 获取图标的 Base64 编码
            icon_base64 = driver.execute_script("""
                var canvas = document.createElement('canvas');
                var img = document.querySelector('img');
                if (!img) return null;
                
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;
                var ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);
                
                return canvas.toDataURL('image/png').split(',')[1];
            """)

            if icon_base64:
                return jsonify({
                    "status": "success",
                    "data": icon_base64
                })
            else:
                logger.error("未找到图标元素")
                return jsonify({"error": "未找到图标元素"}), 404

        except Exception as e:
            logger.error(f"图标提取失败: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            driver.quit()
    except Exception as e:
        logger.error(f"全局异常: {str(e)}")
        return jsonify({"error": "服务器错误"}), 500
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)