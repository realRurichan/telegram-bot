from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode
from loguru import logger
from plugins.CheckMessageTimedOut import CheckTimedOut

def load():
    logger.info("Feedback is loaded.")

FEEDBACK_CHAT_ID = -1001871267220

def get_name(user):
    if user.last_name != None:
        name = user.first_name + user.last_name
        return name
    else:
        return user.first_name

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CheckTimedOut(update, context):
        return
    logger.debug(str(update.to_dict()))
    feedback_content = update.message.text[10: ]
    name = get_name(update.message.from_user)
    link = "tg://user?id=" + str(update.message.from_user.id)
    final_message = f'来自 <a href="{link}">{name}</a> 的反馈：\n' + feedback_content
    await context.bot.send_message(
        chat_id=FEEDBACK_CHAT_ID, text=final_message, parse_mode=ParseMode.HTML
    )
    await update.message.reply_text('反馈已发送w')

handlers = [CommandHandler("feedback", feedback)]