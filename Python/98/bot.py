import logging
import asyncio
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from config import accounts
from login import input_main

# === 日志设置 ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



# === Telegram Bot Token ===
bot_token = "Token"  # ⚠️ 替换为真实 Token

# === 执行日志列表 ===
execution_logs = []

# === /start 指令：显示主菜单 ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ 全部账号签到", callback_data="sign_all")],
        [InlineKeyboardButton("✅ 签到指定账号", callback_data="choose_account")],
    ]
    await update.message.reply_text(
        "请选择签到方式：", reply_markup=InlineKeyboardMarkup(keyboard)
    )

# === /logs 指令：显示最近签到日志 ===
async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not execution_logs:
        await update.message.reply_text("暂无签到记录。")
        return

    latest_logs = execution_logs[-10:]
    text = "\n".join(
        f"[{log['timestamp']}] {log['username']} - {log['status']}"
        for log in latest_logs
    )
    await update.message.reply_text("📜 最近签到记录：\n" + text)

# === 处理按钮点击 ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "sign_all":
        messages = []
        for acc in accounts.values():
            try:
                status = input_main(acc)
                result = f"✅ {acc.username} 成功" if status == "成功" else f"❌ {acc.username} 失败：{status}"
            except Exception as e:
                result = f"❌ {acc.username} 异常：{e}"
                status = str(e)

            messages.append(result)
            execution_logs.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "username": acc.username,
                "status": status,
            })

        await query.edit_message_text("签到结果：\n" + "\n".join(messages))

    elif data == "choose_account":
        keyboard = [
            [InlineKeyboardButton(acc.username, callback_data=f"sign_{acc.username}")]
            for acc in accounts.values()
        ]
        await query.edit_message_text(
            "请选择要签到的账号：", reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("sign_"):
        username = data.removeprefix("sign_")
        acc = accounts.get(username)
        if not acc:
            await query.edit_message_text(f"⚠️ 账号 {username} 未找到。")
            return

        try:
            status = input_main(acc)
            result = f"✅ {acc.username} 成功" if status == "签到成功" or  status == "今日已签到" else f"❌ {acc.username} 失败：{status}"
        except Exception as e:
            result = f"❌ 执行异常：{e}"
            status = str(e)

        execution_logs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": acc.username,
            "status": status,
        })

        await query.edit_message_text(result)

# === 可选：异步每日自动签到（不必须） ===
async def auto_sign_loop():
    while True:
        for acc in accounts.values():
            await asyncio.sleep(random.randint(0, 86400))
            try:
                status = input_main(acc)
            except Exception as e:
                status = f"失败: {e}"
            execution_logs.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "username": acc.username,
                "status": status,
            })

# === 启动 Bot 应用 ===
if __name__ == "__main__":
    try:
        print("✅ 启动中...")
        app = ApplicationBuilder().token(bot_token).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("logs", logs))
        app.add_handler(CallbackQueryHandler(button_handler))


        print("✅ Bot 正在监听中，发送 /start 测试...")
        app.run_polling()
    except Exception as e:
        logger.error(f"❌ Bot 启动失败：{e}")
