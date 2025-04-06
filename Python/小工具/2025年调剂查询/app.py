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
        'Cookie': """JSESSIONID=BC753B38188A83C691537ECA786DF966; _ga_YKHKPH396P=GS1.1.1742893590.1.0.1742893600.0.0.0; Hm_lvt_9c8767bf2ffaff9d16e0e409bd28017b=1743043379; CHSICLTID=CA1.1.4419ed3ef3d4b81fd56369d365f455c6; CHSIDSTID=195cc8d25531de2-0f78f026b324a5-1b525636-1fa400-195cc8d25543344; _abfpc=7e448833ea986d5791d3e102b319236f24218981_2.0; cna=becd8b8092065b35f51856a997125d3f; _ga_RNH4PZV76K=GS1.1.1743043396.1.1.1743043457.0.0.0; _ga_8YMQD1TE48=GS1.1.1743043381.1.1.1743043459.0.0.0; JSESSIONID=DE285E38487B27748EC95FE006330A9F; XSRF-CCKTOKEN=da2b94e7b22adb0f54d5d4ae7eabe64e; CHSICC_CLIENTFLAGYZ=4bdb2e08b81febd11221266939eb90c9; Hm_lvt_3916ecc93c59d4c6e9d954a54f37d84c=1743576292,1743582825,1743604453,1743924071; HMACCOUNT=64B336966BEE4E11; _gid=GA1.3.635064485.1743924071; _ga_TT7MCH8RRF=GS1.1.1743924112.15.0.1743924114.0.0.0; CHSICC_CLIENTFLAGSYTJ=0857739fa9b318e9935e301476043ae2; Hm_lpvt_3916ecc93c59d4c6e9d954a54f37d84c=1743924149; _ga_YZV5950NX3=GS1.1.1743924071.26.1.1743924149.0.0.0; _ga=GA1.1.611441936.1742797364"""
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
    app.run(debug=True,port = 1314)
