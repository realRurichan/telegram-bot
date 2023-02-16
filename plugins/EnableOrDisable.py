from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from loguru import logger
import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()
avaliable_feature = ["welcome", "cancelpin", "captcha"]

def load():
    logger.info("EnableOrDisable is loaded.")

async def enable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(str(update.to_dict()))
    if update.effective_chat.type == "group" or update.effective_chat.type == "supergroup":
        user = await update.effective_chat.get_member(update.effective_user.id)
        if user.status == "administrator" or user.status == "creator":
            table_name = str(update.effective_chat.id)[4: ]
            res = cur.execute("select count(*)  from sqlite_master where type='table' and name =" + "\"" + table_name + "\"" + ";")
            if int(res.fetchone()[0]) == 0:
                cur.execute("CREATE TABLE \"" + table_name + "\"( \
                            COMMAND      TEXT         NOT NULL, \
                            BOOL         BOOLEAN      NOT NULL \
                            );")
                cur.execute("INSERT INTO \"" + table_name + "\" (COMMAND,BOOL) \
                            VALUES ('CANCELPIN', 0);")
                cur.execute("INSERT INTO \"" + table_name + "\" (COMMAND,BOOL) \
                            VALUES ('WELCOME', 0);")
                cur.execute("INSERT INTO \"" + table_name + "\" (COMMAND,BOOL) \
                            VALUES ('CAPTCHA', 0);")
                con.commit()
            legal = False
            try:
                feature_name = context.args[0]
                for features in avaliable_feature:
                    if feature_name == features:
                        legal = True
                if legal:
                    cur.execute("UPDATE \"" + table_name + "\" SET BOOL = 1 WHERE COMMAND LIKE \"" + feature_name + "\";")
                    con.commit()
                    await update.message.reply_text("功能已启用w")
                else:
                    await update.message.reply_text("这不是可以禁用/启用的功能哦～请检查一下quq")
            except (IndexError):
                await update.message.reply_text("用法：\n请在指令后面加上想要禁用的功能\n如（括号内为解释）：\nwelcome（进群欢迎）")
        else:
            await update.message.reply_text("只有群组管理员可以使用此功能哦")
    else:
        await update.message.reply_text("请在群组中使用本功能qwq")
        

async def disable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(str(update.to_dict()))
    if update.effective_chat.type == "group" or update.effective_chat.type == "supergroup":
        user = await update.effective_chat.get_member(update.effective_user.id)
        if user.status == "administrator" or user.status == "creator":
            table_name = str(update.effective_chat.id)[4: ]
            res = cur.execute("select count(*)  from sqlite_master where type='table' and name =" + "\"" + table_name + "\"" + ";")
            if int(res.fetchone()[0]) == 0:
                cur.execute("CREATE TABLE \"" + table_name + "\"( \
                            COMMAND      TEXT         NOT NULL, \
                            BOOL         BOOLEAN      NOT NULL \
                            );")
                cur.execute("INSERT INTO \"" + table_name + "\" (COMMAND,BOOL) VALUES ('CANCELPIN', 0);")
                cur.execute("INSERT INTO \"" + table_name + "\" (COMMAND,BOOL) VALUES ('WELCOME', 0);")
                con.commit()
            legal = False
            try:
                feature_name = context.args[0]
                for features in avaliable_feature:
                    if feature_name == features:
                        legal = True
                if legal:
                    cur.execute("UPDATE \"" + table_name + "\" SET BOOL = 0 WHERE COMMAND LIKE \"" + feature_name + "\";")
                    con.commit()
                    await update.message.reply_text("功能已禁用w")
                else:
                    await update.message.reply_text("这不是可以禁用/启用的功能哦～请检查一下quq")
            except (IndexError):
                await update.message.reply_text("用法：\n请在指令后面加上想要禁用的功能\n如（括号内为解释）：\nwelcome（进群欢迎），cancelpin（取消频道自动置顶）")
        else:
            await update.message.reply_text("只有群组管理员可以使用此功能哦")
    else:
        await update.message.reply_text("请在群组中使用本功能qwq")

handlers = [CommandHandler("enable", enable), CommandHandler("disable", disable)]

    