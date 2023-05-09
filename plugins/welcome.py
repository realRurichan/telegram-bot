from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import ContextTypes, CommandHandler, ChatMemberHandler
from typing import Optional, Tuple
import sqlite3
from loguru import logger
from plugins.CheckMessageTimedOut import CheckTimedOut

con = sqlite3.connect("database.db")
cur = con.cursor()


def load():
    logger.info("WelcomePlugin is loaded.")


async def welcomeset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CheckTimedOut(update, context):
        return
    logger.debug(str(update.to_dict()))
    if (
        update.effective_chat.type == "group"
        or update.effective_chat.type == "supergroup"
    ):
        group_id = str(update.effective_chat.id)[4:]
        res = cur.execute(
            'select BOOL  from "' + group_id + '" where COMMAND = "WELCOME";'
        )
        if int(res.fetchone()[0]) == 1:
            user = await update.effective_chat.get_member(update.effective_user.id)
            if user.status == "administrator" or user.status == "creator":
                res = cur.execute(
                    'SELECT COUNT(*) FROM WELCOME WHERE GROUP_ID = "' + group_id + '";'
                )
                if int(res.fetchone()[0]) == 0:
                    try:
                        match_context = update.message.text[12:]
                        sql_command = (
                            "INSERT INTO WELCOME (GROUP_ID,REPLY) VALUES ("
                            + group_id
                            + ",?);"
                        )
                        cur.execute(sql_command, (match_context,))
                        con.commit()
                        logger.debug("SQL command executed: " + sql_command)
                        text = "欢迎语设置成功w"
                        await update.message.reply_text(text)
                        logger.info("Welcome Plugin replied: " + text)
                    except IndexError:
                        text = "用法：\n请在指令后面加上想要设置的欢迎语w"
                        await update.message.reply_text(text)
                        logger.info("Welcome Plugin replied: " + text)
                else:
                    try:
                        match_context = update.message.text[12:]
                        sql_command = (
                            'UPDATE WELCOME SET REPLY = ? WHERE GROUP_ID = "'
                            + group_id
                            + '";'
                        )
                        cur.execute(sql_command, (match_context,))
                        con.commit()
                        logger.debug("SQL command executed: " + sql_command)
                        text = "欢迎语设置成功w"
                        await update.message.reply_text(text)
                        logger.info("Welcome Plugin replied: " + text)
                    except IndexError:
                        text = "用法：\n请在指令后面加上想要设置的欢迎语w"
                        await update.message.reply_text(text)
                        logger.info("Welcome Plugin replied: " + text)
            else:
                text = "只有管理员才能进行此操作哦"
                await update.message.reply_text(text)
                logger.info("Welcome Plugin replied: " + text)
        else:
            text = "请先使用<code>/enable welcome</code>来启用进群欢迎功能哦"
            await update.message.reply_text(text, parse_mode="HTML")
            logger.info("Welcome Plugin replied: " + text)
    else:
        text = "请在群组中使用本指令qwq"
        await update.message.reply_text(text)
        logger.info("Welcome Plugin replied: " + text)


def extract_status_change(
    chat_member_update: ChatMemberUpdated,
) -> Optional[Tuple[bool, bool]]:
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get(
        "is_member", (None, None)
    )

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


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(str(update.to_dict()))
    group_id = str(update.effective_chat.id)[4:]
    res = cur.execute(
        "select count(*)  from sqlite_master where type='table' and name ="
        + '"'
        + group_id
        + '"'
        + ";"
    )
    if int(res.fetchone()[0]) != 0:
        res = cur.execute(
            'select BOOL  from "' + group_id + '" where COMMAND = "WELCOME";'
        )
        if int(res.fetchone()[0]) == 1:
            group_id = str(update.effective_chat.id)[4:]
            res = cur.execute(
                'select REPLY  from WELCOME where GROUP_ID = "' + group_id + '";'
            )
            result = extract_status_change(update.chat_member)
            if result is None:
                return

            was_member, is_member = result
            cause_name = update.chat_member.from_user.mention_html()
            member_name = update.chat_member.new_chat_member.user.mention_html()

            if not was_member and is_member:
                group_id = str(update.effective_chat.id)[4:]
                res = cur.execute(
                    'select REPLY  from WELCOME where GROUP_ID = "' + group_id + '";'
                )
                try:
                    text = res.fetchone()[0]
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id, text=text
                    )
                    logger.info("Welcome Plugin said: " + text)
                except IndexError:
                    text = "请管理员设置欢迎语qwq"
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id, text=text
                    )
                    logger.info("Welcome Plugin said: " + text)
    else:
        return


"""            
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = str(update.effective_chat.id)[4: ]
    res = cur.execute("select BOOL  from \"" + group_id + "\" where COMMAND = \"WELCOME\";")
    if int(res.fetchone()[0]) == 1:
        group_id = str(update.effective_chat.id)[4: ]
        res = cur.execute("select REPLY  from WELCOME where GROUP_ID = \"" + group_id + "\";")
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=res.fetchone()[0])
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="请管理员设置欢迎语qwq")
"""
handlers = [
    CommandHandler("welcomeset", welcomeset),
    ChatMemberHandler(welcome, ChatMemberHandler.ANY_CHAT_MEMBER),
]
