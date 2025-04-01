import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # 获取前端传递的专业名称，默认为“网络与信息安全”
    zymc = request.form.get('zymc', '网络与信息安全') if request.method == 'POST' else '网络与信息安全'

    # 调用接口并获取数据
    url = 'https://yz.chsi.com.cn/sytj/stu/tjyxqexxcx.action'  # 你实际的接口URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': """cookie"""
    }

    # 这里的分页控制开始
    all_data = []  # 用于存储所有数据
    for start in range(0, 401, 20):  # 从 0 到 200，步长为 20
        payload = {
            'orderBy': '',
            'ssdm': '',
            'dwmc': '',
            'xxfs': '1',  # 使用按页查询
            'zxjh': '0',
            'zymc': zymc,  # 这里动态传递专业名称
            'start': str(start),  # 控制分页
            'pageSize': '20'  # 每页 20 条
        }

        response = requests.post(url, headers=headers, data=payload)

        # 打印响应内容，检查是否为有效的JSON
        print(response.text)

        try:
            # 解析响应数据
            data = response.json()

            # 检查 'vos' 字段是否存在并且非空
            vos_data = data.get('msg', {}).get('data', {}).get('vo_list', {}).get('vos', [])

            if not vos_data:  # 如果没有数据，跳出循环
                break

            all_data.extend(vos_data)  # 添加当前页数据到总数据列表

        except ValueError:
            return f"接口返回的内容不是有效的JSON格式：{response.text}", 500
        except KeyError:
            return f"响应数据缺少预期的字段，可能数据格式发生变化。", 500

    # 返回所有数据到前端
    return render_template('index.html', data=all_data, zymc=zymc)

if __name__ == '__main__':
    app.run(debug=True)
