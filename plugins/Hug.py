from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from loguru import logger
import random
from plugins.CheckMessageTimedOut import CheckTimedOut


def load():
    logger.info("Hug is loaded.")


sentences_list = ["月兔抱抱你哦，希望你能好受一点qwq", "抱抱！希望你能开开心心的w", "小兔子抱抱你w", "抱w 希望我的抱抱能让你开心呢"]

stickers_list = [
    "CAACAgEAAxkBAAIFVmPuvB325FcvBMsVU5ViuDe9Bti3AAIuJwACePzGBWM311IX5pd8LgQ",
    "CAACAgEAAxkBAAIFWmPuvD0JWDFaj4zwrSqI7D_oUrz6AAKhKAACePzGBUqlR20jxOiyLgQ",
]


async def hug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CheckTimedOut(update, context):
        return
    logger.debug(str(update.to_dict()))
    reply_sentence = sentences_list[random.randint(0, 3)]
    reply_sticker = stickers_list[random.randint(0, 1)]
    await context.bot.send_sticker(
        chat_id=update.effective_chat.id, sticker=reply_sticker
    )
    await update.message.reply_text(reply_sentence)


handlers = [CommandHandler("hug", hug)]
