from flask import Flask, request, jsonify
 # 确保路径正确
import logging

from web_scan.WebsiteScanner import WebsiteScanner

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': '缺少 "url" 参数'}), 400

    target_url = data['url']

    scanner = WebsiteScanner(target_url)
    results = scanner.scan_website()

    return jsonify(results), 200

if __name__ == '__main__':
    app.config['JSON_SORT_KEYS'] = False
    app.run(host='0.0.0.0', port=5000)