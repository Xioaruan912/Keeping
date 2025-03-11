import base64

from flask import Flask, request, jsonify
from loguru import logger

from spider.main_spider import main_spider, clean_json_string

app = Flask(__name__)
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    url = data.get('url')
    if not url:
        return jsonify({"error": "'url' 是必填字段"}), 400

    # 解码 post_data 和 headers（如果存在）
    decoded_post_data = data.get('post_data')
    if decoded_post_data:
        decoded_post_data = clean_json_string(base64.b64decode(decoded_post_data).decode('utf-8'))
        logger.success(decoded_post_data)
    decoded_headers = data.get('headers')
    if decoded_headers:
        decoded_headers = clean_json_string(base64.b64decode(decoded_headers).decode('utf-8'))
        logger.success(decoded_headers)
    # 调用爬虫函数获取原始响应内容
    try:
        raw_response = main_spider(url, decoded_post_data, decoded_headers)
        # 直接返回原始响应内容，不修改结构
        return raw_response, 200, {'Content-Type': 'application/json'}  # 根据实际响应类型调整 Content-Type
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)