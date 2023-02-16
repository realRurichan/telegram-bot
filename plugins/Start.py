from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from loguru import logger

def load():
    logger.info("Hello is loaded.")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker(sticker="CAACAgEAAx0CRPBUlQABAglRY-i_DEePN_fT8f0tOb4-6pUFHF0AAmQnAAJ4_MYFUqxli8Dq4fcuBA")

handlers = [CommandHandler(['hello','hi','start'], hello)]