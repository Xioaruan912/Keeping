import json
import random
import time

import requests
from loguru import logger

import Get_url


def Get_access_token():
    # pro = {
    #     "http":"http://127.0.0.1:8080",
    #     "https": "http://127.0.0.1:8080"
    # }
    header  = {
        "Connection": "Keep-Alive"
    }
    time_now = time.time()
    url = Get_url.G_u()
    response = requests.post(url,headers=header)
    response_data = json.loads(response.content)
    access_token = response_data.get("access_token")
    logger.success("获取access_token----"+access_token)
    return  access_token
def Get_Key(access_token):
    logger.info("开始获取userid")
    url = f"http://api.vbskit.com:58080/reguser?access_token={access_token}"
    deviceserid = random.randint(1000000, 99999999999999999)
    body = {
        "deviceserid": f"{deviceserid}",
        "barnd": "vivo",
        "model": "V1938T",
        "cpua": "Hardware\t: placeholder",
        "sysversion": "5.1.1",
        "acf": 0,
        "clf": 1,
        "arfcn": 0,
        "softversion": "1.6.7",
        "androidid": "2ba712f0c3a9c3c3"
    }
    header = {
        "Content-Encoding": "UTF-8",
        "Content-Type": "application/json"
    }
    response = requests.post(url=url, headers=header, json=body)
    response_data = json.loads(response.content)

    # 添加 access_token 到响应
    response_data["access_token"] = access_token

    logger.info(response_data)
    isfirst = response_data.get("isfirst")
    userid = response_data.get("userid")
    logger.info("获取userid----" + str(userid))
    return isfirst, userid
def repprovince(access_token,userid):  #获取认证

    logger.info("开始认证")
    header = {
        "Content-Encoding":"""UTF-8""",
        "Content-Type":"application/json"
    }
    url = f"http://api.vbskit.com:58080/repprovince?access_token={access_token}"
    body = {
        "userid": userid,
        "province": "%u5317%u4eac", "profession": "%u4e2d%u56fd"
    }
    response = requests.post(url=url,headers=header,json=body)

    logger.info("认证结果" + str(response.content))
    return response.content

def Wifi_Get(access_token,userid):
    pro = {
        "http":"http://127.0.0.1:7897",
        "https": "http://127.0.0.1:7897"
    }
    url = f"""http://api.vbskit.com:58080/wifiquery?access_token={access_token}"""
    time.sleep(1)
    mac = "00:81:bb:51:db:b9"
    body = {
        "mac": f"{mac}",
        "userid": userid
    }
    header = {
        "Content-Encoding":"""UTF-8""",
        "Content-Type":"application/json"
    }
    response = requests.post(url=url,headers=header,json=body,proxies=pro)
    if response.status_code == 200:
        response_data = response.json()
        formatted_json = json.dumps(response_data, indent=4, ensure_ascii=False)
        print(formatted_json)



if __name__ == '__main__':
    while(1):
        access_token = Get_access_token()
        isfirst,userid = Get_Key(access_token)
        if(isfirst != 1):
            logger.info("不是第一次")
        check = repprovince(access_token,userid)
        Wifi_Get(access_token,userid)