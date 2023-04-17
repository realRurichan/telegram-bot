from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from loguru import logger
import sqlite3
import asyncio

con = sqlite3.connect("database.db")
cur = con.cursor()

def load():
    logger.info("CancelPin is loaded.")

async def cancelpin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(str(update.to_dict()))
    group_id = str(update.effective_chat.id)[4: ]
    res = cur.execute("select BOOL  from \"" + group_id + "\" where COMMAND = \"CANCELPIN\";")
    if int(res.fetchone()[0]) == 1:
        await asyncio.sleep(30)
        await context.bot.get_me()
        result = await context.bot.unpin_chat_message(update.effective_message.chat.id, update.effective_message.message_id)
        if result == True:
            logger.debug("Auto Unpin OK!")
        else:
            raise Exception('Auto Unpin Failed!')
    else:
        return



handlers = [MessageHandler(filters.IS_AUTOMATIC_FORWARD, cancelpin)]