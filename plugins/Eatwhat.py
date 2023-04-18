from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from loguru import logger
import linecache
import random
from plugins.CheckMessageTimedOut import CheckTimedOut


def load():
    logger.info("Eatwhat is loaded.")


async def eatwhat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CheckTimedOut(update, context):
        return
    result = linecache.getline("datas/eats.lst", random.randint(1, 133))
    await update.message.reply_text("咕噜咕噜，让小兔子告诉你吃什么吧w：\n" + "今天吃" + result)


handlers = [CommandHandler(["eatwhat"], eatwhat)]
