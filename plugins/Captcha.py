from telegram import Update, Chat, ChatMember, ChatMemberUpdated
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ChatMemberHandler, ConversationHandler, MessageHandler, filters
import plugins as bot_plugins
from typing import Optional, Tuple
import re
import sqlite3
from loguru import logger

con = sqlite3.connect("database.db")
cur = con.cursor()
message = None

PASS_CAPTCHA = range(1)

def load():
    logger.info("CaptchaPlugin is loaded.")

def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:

    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)
    return was_member, is_member

async def captcha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(str(update.to_dict()))
    group_id = str(update.effective_chat.id)[4: ]
    res = cur.execute("select count(*)  from sqlite_master where type='table' and name =" + "\"" + group_id + "\"" + ";")
    if int(res.fetchone()[0]) != 0:
        result = extract_status_change(update.chat_member)
        if result is None:
            return ConversationHandler.END
        was_member, is_member = result
        if not was_member and is_member:
            global message
            message = await context.bot.send_message(chat_id=update.effective_chat.id, text='你好～欢迎来到本群！为了验证你是真人，请发送一个 Sticker（表情）来通过验证w')
            return PASS_CAPTCHA
        else: return ConversationHandler.END
    else: return ConversationHandler.END

async def pass_captcha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await message.delete()
    await update.message.reply_text('好诶，是新朋友w')
    return ConversationHandler.END

async def not_pass_captcha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()

handlers = [ConversationHandler(
        entry_points=[ChatMemberHandler(captcha, ChatMemberHandler.ANY_CHAT_MEMBER)],
        states={
            PASS_CAPTCHA: [MessageHandler(filters.Sticker.ALL, pass_captcha),],
        },
        fallbacks=[MessageHandler(None, not_pass_captcha),],
    )]