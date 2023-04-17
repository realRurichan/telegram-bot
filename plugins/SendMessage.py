import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
from telegram.constants import ParseMode
from loguru import logger

load_dotenv()

def load():
    logger.info("SendMessage is loaded.")

admin_id = os.getenv("ADMIN_ID")
target_chat_id = 0
GETMESSAGE = range(1)

async def sendmessage_get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(str(update.to_dict()))
    print(admin_id)
    print(update.effective_user.id)
    if int(update.effective_user.id) == int(admin_id):
        global target_chat_id 
        try:
            target_chat_id = int(context.args[0])
            print(target_chat_id)
        except:
            await update.message.reply_text('请输入对方的ID哦')
            return ConversationHandler.END
        await update.message.reply_text('收到w，那么要发送什么内容呢？可以使用 <code>/cancel</code> 取消哦', parse_mode=ParseMode.HTML)
        return GETMESSAGE
    else:
        return ConversationHandler.END

async def sendmessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(str(update.to_dict()))
    await update.message.copy(target_chat_id)
    await update.message.reply_text('信息发送成功w')
    return ConversationHandler.END

async def cancel_sendmessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(str(update.to_dict()))
    await update.message.reply_text('已取消w')
    return ConversationHandler.END

handlers = [ConversationHandler(entry_points=[CommandHandler("send", sendmessage_get_id)], 
            states={GETMESSAGE:[MessageHandler(~filters.Regex("^\/cancel$"), sendmessage)]},
            fallbacks=[CommandHandler("cancel", cancel_sendmessage)],)]