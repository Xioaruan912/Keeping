import time

import requests
from flask import Flask, render_template, request
from reques_web import re,get_data
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    all_data,zymc = get_data()
    return render_template('index.html', data=all_data, zymc=zymc)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 2000)
