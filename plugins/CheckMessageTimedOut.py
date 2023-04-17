from loguru import logger
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import ContextTypes

def load():
    logger.info("CheckMessageTimedOut module is loaded")

def CheckTimedOut(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_time = datetime.now(timezone.utc)
    message_time = update.message.date

    time_difference = (current_time - message_time).total_seconds()

    # 设置一个阈值，例如5秒
    time_threshold = 5

    if time_difference > time_threshold:
        logger.debug("Ignoring old message.")
        return True

    # 如果消息未被忽略，将其传递给其他处理器
    return False

handlers = []