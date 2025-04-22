from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from threading import Thread
from datetime import datetime, timedelta
import random
import time
from config import PASSWORD, accounts  # 从 config 导入密码
from login import input_main

# 初始化 Flask 应用
app = Flask(__name__)

# 配置 SQLite 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sign_in.db'  # SQLite 数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用对象修改追踪

# 设置 Flask 密钥，用于加密 session
app.secret_key = 'your_secret_key'  # 用强随机密钥替换

# 初始化数据库对象
db = SQLAlchemy(app)

# 创建数据库模型，用于保存签到记录
class SignInLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<SignInLog {self.username} {self.status}>"

# 修改生成随机时间函数，范围改为凌晨 2 点到 6 点
def generate_random_run_time():
    """生成从今天凌晨 2 点到 6 点之间的随机时间"""
    now = datetime.now()
    today_2am = datetime(now.year, now.month, now.day, 2, 0, 0)  # 今天凌晨 2 点
    rand_secs = random.randint(0, 14400)  # 随机生成 0 到 14400 秒之间的时间（即 0 到 4 小时）
    scheduled = today_2am + timedelta(seconds=rand_secs)
    
    if scheduled <= now:
        scheduled = today_2am + timedelta(days=1, seconds=random.randint(0, 14400))
    
    return scheduled

def get_next_run_times():
    """生成每个账号的下次执行时间"""
    return {acc.username: generate_random_run_time() for acc in accounts.values()}

# --- 密码验证路由 ---
@app.route("/check_password", methods=["POST"])
def check_password():
    """验证输入的密码"""
    password = request.form.get("password")
    
    if password == PASSWORD:
        session['logged_in'] = True  # 设置登录状态
        return redirect(url_for('home'))  # 密码正确跳转到主页
    else:
        flash("密码错误，请重试", "danger")
        return redirect(url_for('login'))  # 密码错误返回登录页

@app.route("/login")
def login():
    """登录页：输入密码弹窗"""
    if session.get('logged_in'):
        return redirect(url_for('home'))  # 已经登录跳转到主页
    return render_template("login.html")  # 显示输入密码界面

# --- 主页路由 ---
@app.route("/", methods=["GET", "POST"])
def home():
    """主页：手动签到和查看历史记录"""
    # 如果未登录，则跳转到密码输入页面
    if not session.get('logged_in'):
        return redirect(url_for('login')) 

    message = ""
    if request.method == "POST":
        selected_username = request.form.get("selected_account")
        acc = accounts.get(selected_username)
        if acc:
            try:
                status = input_main(acc)
                # 将签到记录保存到数据库
                sign_in_log = SignInLog(
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    username=acc.username,
                    status=status
                )
                db.session.add(sign_in_log)
                db.session.commit()

                message = f"手动签到成功：{acc.username}"
            except Exception as e:
                message = f"手动签到失败：{e}"
        else:
            message = "未找到该账号！"

    # 从数据库加载历史签到记录
    logs = SignInLog.query.all()
    next_run_times = get_next_run_times()  # 获取下次执行时间

    return render_template(
        "index.html",
        logs=logs,
        accounts=accounts.keys(),
        next_run_times=next_run_times,
        message=message
    )

@app.route("/run_all", methods=["POST"])
def run_all():
    """处理“全部签到”请求"""
    message = ""
    for acc in accounts.values():
        try:
            status = input_main(acc)
            # 将签到记录保存到数据库
            sign_in_log = SignInLog(
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                username=acc.username,
                status=status
            )
            db.session.add(sign_in_log)
            db.session.commit()
        except Exception as e:
            sign_in_log = SignInLog(
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                username=acc.username,
                status=f"失败: {e}"
            )
            db.session.add(sign_in_log)
            db.session.commit()

    message = "全部签到已执行"
    return redirect(url_for('home', message=message))

@app.route("/auto_sign_in", methods=["POST"])
def auto_sign_in():
    """自动签到逻辑：如果签到状态为“系统繁忙”，则重新生成下次签到时间"""
    message = ""
    
    # 遍历所有账号进行自动签到
    for acc in accounts.values():
        while True:  # 循环尝试，直到签到成功
            status = input_main(acc)  # 获取签到状态
            if status == "系统繁忙":
                # 如果状态是系统繁忙，重新生成下次执行时间并重试
                next_run_time = generate_random_run_time()
                print(f"系统繁忙，重新生成下次时间：{next_run_time}")
                time.sleep(10)  # 等待 10 秒后再尝试
                continue  # 重试
            
            # 如果签到成功或失败，保存签到记录
            sign_in_log = SignInLog(
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                username=acc.username,
                status=status
            )
            db.session.add(sign_in_log)
            db.session.commit()
            break  # 跳出循环，继续下一个账号

    message = "自动签到已完成"
    return redirect(url_for('home', message=message))

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 

    app.run(host="0.0.0.0", port=2000)
