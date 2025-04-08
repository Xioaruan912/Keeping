from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from reques_web import get_data
import logging

YOUR_BOT_TOKEN = "7943600651:AAGOwiT0iCinaimtYq_aIosIvWBTFD-xTJ8"

# 配置日志
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def escape_markdown_v2(text):
    """转义所有MarkdownV2特殊字符"""
    if not text:
        return ""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join('\\' + char if char in escape_chars else char for char in str(text))


def clean_text(text):
    """清理文本并转义特殊字符"""
    if not text:
        return "无"
    text = str(text).replace('\r\n', ' ').replace('\n', ' ').strip()
    return escape_markdown_v2(text)


def format_data(data, zymc):
    """格式化调剂信息，显示全部数据"""
    if not data or not isinstance(data, list):
        return "⚠️ 未查询到有效的调剂信息"

    message = f"🔍 *2025年研究生调剂信息* \\${zymc}\\$专业\n\n"

    for item in data:
        school = clean_text(item.get('dwmc', '未知学校'))
        college = clean_text(item.get('yxsmc', '未知学院'))
        quota = item.get('qers', 0)
        status = clean_text(item.get('zt', '未知状态'))
        time = clean_text(item.get('fbsjStr', '未知时间'))
        requirements = clean_text(item.get('bz', '无'))

        school = school.replace("-", "—")

        message += (
            f"🏛 *{school}*\n"
            f"  \\• 学院\\: {college}\n"
            f"  \\• 调剂余额\\: {quota}人\n"
            f"  \\• 状态\\: {status}\n"
            f"  \\• 发布时间\\: {time}\n"
            f"  \\• 要求\\: {requirements}\n\n"
        )

    message += f"📊 共找到 {len(data)} 条记录\n"
    message += "💡 提示\\: 发送 `/l  专业名称` 查询其他专业"
    return message


async def send_adjustment_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /adjust 命令"""
    try:
        user_id = update.message.from_user.id
        logger.info(f"用户 {user_id} 请求调剂信息")

        # 获取用户输入的专业（默认为"网络与信息安全"）
        zymc = "网络与信息安全"  # 默认值
        if context.args:
            zymc = ' '.join(context.args).strip()
            logger.info(f"用户指定专业: {zymc}")

        print(f"⏳ 正在获取【{zymc}】专业数据...")
        data, returned_zymc = get_data(zymc)

        if data is None:
            await update.message.reply_text("❌ 获取数据失败，请稍后重试")
            return

        print(f"✅ 获取到 {len(data)} 条{returned_zymc}专业数据")
        message = format_data(data, returned_zymc)

        # 分片发送长消息
        max_length = 4000
        for i in range(0, len(message), max_length):
            chunk = message[i:i + max_length]
            await update.message.reply_text(
                chunk,
                parse_mode="MarkdownV2",
                disable_web_page_preview=True
            )
        print("📤 消息已发送")

    except Exception as e:
        logger.error(f"错误: {e}")
        await update.message.reply_text("❌ 发生错误，请检查输入格式：/l 专业名称")


def main():
    print("🤖 Bot 启动中...")
    application = Application.builder().token(YOUR_BOT_TOKEN).build()
    application.add_handler(CommandHandler("l", send_adjustment_info))
    application.run_polling()


if __name__ == "__main__":
    main()