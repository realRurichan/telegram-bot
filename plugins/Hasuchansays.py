from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from loguru import logger
import linecache
import base64
import random
from plugins.CheckMessageTimedOut import CheckTimedOut


def load():
    logger.info("Hasuchansays is loaded.")
    

async def hasuchansays(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CheckTimedOut(update, context):
        return
    result = linecache.getline('datas/quotes.lst', random.randint(1,131))
    await update.message.reply_text("咕噜咕噜，这次又有什么莲子语录呢：\n" + str(base64.b64decode(result), "utf-8"))

handlers = [CommandHandler(['hasuchansays'], hasuchansays)]
