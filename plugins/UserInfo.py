from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from loguru import logger

def load():
    logger.info("UserInfo is loaded.")

async def userinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(str(update.to_dict()))
    if update.message.reply_to_message == None:
        userinfo = update.effective_user
    else:
        userinfo = update.message.reply_to_message.from_user
    
    await update.message.reply_text("<code>" + str(userinfo.to_dict()) + "</code>", parse_mode="HTML")

handlers = [CommandHandler("userinfo", userinfo)]
