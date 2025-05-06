'''
作者: Xioaruan912 xioaruan@gmail.com
最后编辑人员: Xioaruan912 xioaruan@gmail.com
文件作用介绍: 
 单接口模式
'''
from flask import Flask, Response
from config import accounts         # accounts 原本的键是 "NodeAI"、"NodeAII"
from login import input_main        # 执行签到的函数

# 将 accounts 键全部转成小写，方便路由和 config 对齐
accounts = { key.lower(): acc for key, acc in accounts.items() }

app = Flask(__name__)

def do_sign(username: str) -> Response:
    acc = accounts.get(username)
    if not acc:
        return Response("error", status=404)
    try:
        status = input_main(acc)
        # 可根据 status 的具体内容再精细判断
        return Response("ok", status=200)
    except Exception as e:
        app.logger.error(f"签到[{username}] 出错：{e}")
        return Response("error", status=500)

@app.route('/sign/nodeai', methods=['GET'])
def sign_nodeai():
    return do_sign('nodeai')

@app.route('/sign/nodeaii', methods=['GET'])
def sign_nodeaii():
    return do_sign('nodeaii')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)
