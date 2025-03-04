import json
import random
import time

import requests
from loguru import logger

def Get_access_token():
    time_now = time.time()
    url = """http://api.vbskit.com:58080/token?app_id=289541&app_secret=c4de9cf7a84678d01ba19a8f9627bbe0&timestamp=1741068768&nonce=56bbb795-342e-4271-b91a-abd1ecffe5b7&signature=8D36E3E584003FA6C433030226AA1ECDF69D98B6"""
    response = requests.post(url)
    response_data = json.loads(response.content)
    access_token = response_data.get("access_token")
    logger.success("获取access_token----"+access_token)
    return  access_token
def Get_Key(access_token):
    logger.info("开始获取userid")

    url  = f"http://api.vbskit.com:58080/reguser?access_token={access_token}"
    deviceserid = random_number = random.randint(1000000, 99999999)
    body = {
    "deviceserid": f"{deviceserid}",
    "barnd": "samsung",
    "model": "SM-N9700",
    "cpua": "Hardware\t: placeholder",
    "sysversion": "5.1.1",
    "acf": 0,
    "clf": 1,
    "arfcn": 0,
    "softversion": "1.6.7",
    "androidid": "2ba712f0c3a9c3c3"
    }
    header = {
        "User-Agent":"""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36""",
        "Content-Type":"application/json"
    }
    response = requests.post(url=url,headers=header,json=body)
    response_data = json.loads(response.content)
    isfirst = response_data.get("isfirst")
    userid = response_data.get("userid")
    logger.info("获取userid----"+str(userid))
    return  isfirst,userid

def repprovince(access_token,userid):  #获取认证
    logger.info("开始认证")
    header = {
        "User-Agent":"""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36""",
        "Content-Type":"application/json"
    }
    url = f"http://api.vbskit.com:58080/repprovince?access_token={access_token}"
    body = {
        "userid": userid,
        "province": "beijing",
        "profession": "safe"
    }
    response = requests.post(url=url,headers=header,json=body)
    logger.info("认证结果" + str(response.content))
    return response.content

def Wifi_Get(access_token,userid):
    url = f"""http://api.vbskit.com:58080/wifiquery?access_token={access_token}"""
    time.sleep(1)
    mac = input("输入mac地址:")
    body = {
        "mac": f"{mac}",
        "userid": userid
    }
    header = {
        "User-Agent":"""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36""",
        "Content-Type":"application/json"
    }
    response = requests.post(url=url,headers=header,json=body)
    if response.status_code == 200:
        response_data = response.json()
        formatted_json = json.dumps(response_data, indent=4, ensure_ascii=False)
        print(formatted_json)



if __name__ == '__main__':
    access_token = Get_access_token()
    isfirst,userid = Get_Key(access_token)
    if(isfirst != 1):
        isfirst, userid = Get_Key(access_token)
    check = repprovince(access_token,userid)
    Wifi_Get(access_token,userid)