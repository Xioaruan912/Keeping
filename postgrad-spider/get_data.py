import json
import os

import requests
from loguru import logger
def get_code(result):
    url = 'https://yz.chsi.com.cn/zsml/rs/yjfxs.do'
    data = {
        'zydm': '085412',  # 专业代码
        'zymc': '网络与信息安全',  # 专业名称
        'dwdm': result[0],  # 单位代码
        'xxfs': '',  # 学习方式为空
        'dwlxs[0]': 'all',  # 单位类型为 "all"
        'tydxs': '',  # 统一代码显示为空
        'jsggjh': '',  # 教师或教学计划为空
        'start': '0',  # 起始索引
        'pageSize': '3',  # 每页大小
        'totalCount': '0'  # 总数
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        response.raise_for_status()
        res = response.json()

        if 'msg' in res and 'list' in res['msg']:
            for school in res['msg']['list']:
                nzsrs = school.get('nzsrs')
                nzsrsstr = school.get('nzsrsstr')
                kskmz = school.get('kskmz', [])
                kskmdm = school.get('kskmdm', [])
                exam_subjects = {}
                if kskmz:
                    exam_subjects['科目1'] = {
                        '代码': kskmz[0].get('km1Vo', {}).get('kskmdm', '无'),
                        '名称': kskmz[0].get('km1Vo', {}).get('kskmmc', '无'),
                        '备注': kskmz[0].get('km1Vo', {}).get('cksm', '无')
                    }
                    exam_subjects['科目2'] = {
                        '代码': kskmz[0].get('km2Vo', {}).get('kskmdm', '无'),
                        '名称': kskmz[0].get('km2Vo', {}).get('kskmmc', '无'),
                        '备注': kskmz[0].get('km2Vo', {}).get('cksm', '无')
                    }
                    exam_subjects['科目3'] = {
                        '代码': kskmz[0].get('km3Vo', {}).get('kskmdm', '无'),
                        '名称': kskmz[0].get('km3Vo', {}).get('kskmmc', '无'),
                        '备注': kskmz[0].get('km3Vo', {}).get('cksm', '无')
                    }
                    exam_subjects['科目4'] = {
                        '代码': kskmz[0].get('km4Vo', {}).get('kskmdm', '无'),
                        '名称': kskmz[0].get('km4Vo', {}).get('kskmmc', '无'),
                        '备注': kskmz[0].get('km4Vo', {}).get('cksm', '无')
                    }

                school_data = {
                    '拟招收人数': nzsrs,
                    '拟招收人数str': nzsrsstr,
                    '科目代码': kskmdm,
                    '考试科目': exam_subjects
                }
                result.append(school_data)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return result


# 抓取数据并保存到本地文件
def fetch_and_save_data():
    url = 'https://yz.chsi.com.cn/zsml/rs/zydws.do'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0'
    }

    data_f = []
    for ssdm in range(11, 71):
        data = {
            'zydm': '085412',
            'zymc': '网络与信息安全',
            'dwmc': '',
            'dwdm': '',
            'ssdm': str(ssdm),
            'xxfs': '',
            'dwlxs[0]': 'all',
            'tydxs': '',
            'jsggjh': '',
            'start': '0',
            'curPage': '1',
            'pageSize': '10',
            'totalPage': '10',
            'totalCount': '91'
        }

        try:
            response = requests.post(url, data=data, headers=headers)
            response_data = response.json()
            results = []
            for school in response_data['msg']['list']:
                dwdm = school.get('dwdm')
                dwmc = school.get('dwmc')
                szss = school.get('szss')
                results.append([dwdm, dwmc, szss])
            if results:
                for result in results:
                    fetched_data = get_code(result)
                    data_f.append(fetched_data)
                    # logger.info(fetched_data)
        except json.JSONDecodeError:
            print(f"ssdm={ssdm} 的响应内容: 无法解析 JSON 数据")
    logger.info("保存到本地")
    # 将数据保存到本地 JSON 文件
    # logger.info(data_f)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 使用绝对路径测试
    file_path = os.path.join(current_dir, 'data_f.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data_f, f, ensure_ascii=False, indent=4)
    logger.success("保存成功")
    return file_path