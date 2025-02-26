import os.path
import time

from loguru import logger
from flask import Flask, jsonify, render_template
import json

from get_data import fetch_and_save_data

app = Flask(__name__)

# 从本地文件加载数据
def load_data_from_file():
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

@app.route('/')
def index():
    # 显示首页，包含表格数据
    return render_template('index.html')

@app.route('/data')
def get_data():
    # 返回保存的本地文件数据
    data_f = load_data_from_file()
    return jsonify(data_f)

# 新的路由用于显示数据分析页面
@app.route('/analysis')
def analysis():
    # 显示数据分析页面
    return render_template('analysis.html')

if __name__ == '__main__':
    file_path = fetch_and_save_data()
    app.run(debug=True, host='0.0.0.0',port=1234)
