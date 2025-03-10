import hashlib
import time
import uuid
from urllib.parse import urlencode


def generate_signature(app_id, app_secret, sign_key, timestamp, nonce):
    # 将参数放入列表
    params = [str(app_id), app_secret, sign_key, str(timestamp), nonce]


    # 对列表进行字典序排序
    params.sort()


    # 用换行符拼接排序后的参数
    sign_data = "\n".join(params)


    # 计算 SHA-1 哈希值
    sha1 = hashlib.sha1()
    sha1.update(sign_data.encode("utf-8"))
    signature = sha1.hexdigest().upper()


    return signature


def G_u():
    app_id = 289541
    app_secret = "c4de9cf7a84678d01ba19a8f9627bbe0"
    sign_key = "vbskit167"

    # 随机生成 timestamp 和 nonce
    timestamp = int(time.time())  # 当前时间戳
    nonce = str(uuid.uuid4())  # 随机 UUID

    # 生成签名
    signature = generate_signature(app_id, app_secret, sign_key, timestamp, nonce)

    # 构造完整 URL
    base_url = "http://api.vbskit.com:58080/token"
    params = {
        "app_id": app_id,
        "app_secret": app_secret,
        "timestamp": timestamp,
        "nonce": nonce,
        "signature": signature
    }
    full_url = f"{base_url}?{urlencode(params)}"
    print(full_url)
    return  full_url