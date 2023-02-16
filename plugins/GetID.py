from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from loguru import logger

def load():
    logger.info("GetID is loaded.")

async def getid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(str(update.to_dict()))
    if update.message.reply_to_message == None:
        userid = update.effective_user.id
    else:
        userid = update.message.reply_to_message.from_user.id

    await update.message.reply_text("用户ID为" + str(userid))

handlers = [CommandHandler("getid", getid)]
