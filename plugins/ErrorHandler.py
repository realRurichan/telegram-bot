from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.constants import ParseMode
from loguru import logger
import traceback
import html
import json

DEVELOPER_CHAT_ID = -1001645682861

def load():
    logger.info("ErrorHandle is loaded.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update: " + str(context.error))

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    try:
        message = (
            f"呜呜呜我发生了一个错误，琉璃妈妈快来看看：\n"
            f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
            "</pre>\n\n"
            f"<pre>context.chat_data = {html.escape(str(update.effective_user.to_dict()))}</pre>\n\n"
            f"<pre>context.user_data = {html.escape(str(update.effective_chat.to_dict()))}</pre>\n\n"
            f"<pre>{html.escape(tb_string)}</pre>"
        )
    except:
        message = (
            f"呜呜呜我发生了一个错误，琉璃妈妈快来看看：\n"
            f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
            "</pre>\n\n"
            f"<pre>{html.escape(tb_string)}</pre>"
        )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )

handlers = []
