from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from loguru import logger
from plugins.CheckMessageTimedOut import CheckTimedOut

def load():
    logger.info("FeedPlugin is loaded.")

def get_name(user):
    if user.last_name != None:
        name = user.first_name + user.last_name
        return name
    else:
        return user.first_name

async def feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CheckTimedOut(update, context):
        return
    logger.debug(str(update.to_dict()))
    get_me = await context.bot.get_me()
    bot_id = get_me.id
    if update.effective_message.reply_to_message == None or update.effective_message.reply_to_message.from_user.id == bot_id:
        name = get_name(update.effective_user)
        link = "tg://user?id=" + str(update.effective_user.id)
        await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker="CAACAgEAAx0CRPBUlQABAhw0Y-4ys7vbDlqNu6zZsH-5G01ng1wAAlMiAAJ4_MYFMXNJLW1xiSsuBA")
        await update.message.reply_text(f'感谢 <a href="{link}">{name}</a> 送给月兔的胡萝卜一根喵w', parse_mode="HTML")
    else:
        ori_name = get_name(update.effective_user)
        target_name = get_name(update.effective_message.reply_to_message.from_user)
        ori_link = "tg://user?id=" + str(update.effective_user.id)
        target_link = "tg://user?id=" + str(update.effective_message.reply_to_message.from_user.id)
        if ori_name == target_name:
            await update.message.reply_text(f'唔，<a href="{ori_link}">{ori_name}</a> 喂了自己一根胡萝卜呢，好奇怪的指令呢。', parse_mode="HTML")
            return
        await update.message.reply_text(f'唔，<a href="{ori_link}">{ori_name}</a> 喂了 <a href="{target_link}">{target_name}</a> 一根胡萝卜呢，但这是属于小兔子的食物，对方会不会爱吃呢...', parse_mode="HTML")

handlers = [CommandHandler("feed", feed)]