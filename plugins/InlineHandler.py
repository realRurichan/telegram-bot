from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes, InlineQueryHandler
from loguru import logger
import plugins.InlinePlugins as InlinePlugins
import re

def load():
    logger.info("InlineHandler is loaded")

async def InlineHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(f'Got inline query:\'{update.inline_query.query}\'')
    query = update.inline_query.query
    for plugin in InlinePlugins.__all__:
        if plugin.match(query):
            await plugin.main(update, context)

handlers = [InlineQueryHandler(InlineHandler)]