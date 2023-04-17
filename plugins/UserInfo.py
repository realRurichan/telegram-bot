from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from loguru import logger
from plugins.CheckMessageTimedOut import CheckTimedOut

def load():
    logger.info("UserInfo is loaded.")

async def userinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CheckTimedOut(update, context):
        return
    logger.debug(str(update.to_dict()))
    if update.message.reply_to_message == None:
        userinfo = update.effective_user
    else:
        userinfo = update.message.reply_to_message.from_user
    
    await update.message.reply_text("<code>" + str(userinfo.to_dict()) + "</code>", parse_mode="HTML")

handlers = [CommandHandler("userinfo", userinfo)]
