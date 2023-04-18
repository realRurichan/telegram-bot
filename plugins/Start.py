from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from loguru import logger
from plugins.CheckMessageTimedOut import CheckTimedOut


def load():
    logger.info("Hello is loaded.")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CheckTimedOut(update, context):
        return
    logger.debug(str(update.to_dict()))
    await update.message.reply_sticker(
        sticker="CAACAgEAAx0CRPBUlQABAglRY-i_DEePN_fT8f0tOb4-6pUFHF0AAmQnAAJ4_MYFUqxli8Dq4fcuBA"
    )


handlers = [CommandHandler(["hello", "hi", "start"], hello)]
