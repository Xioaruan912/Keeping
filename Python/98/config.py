'''
作者: Xioaruan912 xioaruan@gmail.com
最后编辑人员: Xioaruan912 xioaruan@gmail.com
文件作用介绍: 

'''
import random

class ACC:
    def __init__(self, username, password, question, pinluns):
        self.username = username
        self.password = password
        self.question = question
        self.pinlun = random.choice(pinluns) if isinstance(pinluns, list) else pinluns
PASSWORD = '密码'
# 多账号配置
accounts = {
    "账号名称": ACC(
        username="账号名称",
        password="密码",
        question="问题答案",
        pinluns=[
            "感谢分享！！！！！",
            "谢谢楼主~",
            "冲冲冲！",
            "来了来了！",
            "感谢分享！！",

        ],
    ),
}
