from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from loguru import logger
import re

regex = (
    r"(?:https?:\/\/)?(?:www\.)?(?:twitter\.com|x\.com)\/(?:#!\/)?(\w+)\/status?\/(\w+)"
)


def match(query: str):
    result = re.match(regex, query)
    if result:
        logger.debug(f"Matched")
    return result


async def main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    logger.debug(f"Matched: {query}")
    pattern = r"/(?:www\.|mobile\.)?(?:twitter\.com|x\.com)/([^/]+/status/\d{19})"
    match = re.search(pattern, query)
    if match:
        tweet_id = match.group(1)
        fxtweet_link = f"https://fxtwitter.com/{tweet_id}"
        results = [
            InlineQueryResultArticle(
                id="1",
                title="Fxtweet Share",
                input_message_content=InputTextMessageContent(fxtweet_link),
                description=fxtweet_link,
                thumb_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Logo_of_Twitter%2C_Inc..svg/584px-Logo_of_Twitter%2C_Inc..svg.png",
            )
        ]
        await context.bot.answer_inline_query(update.inline_query.id, results)
    else:
        await context.bot.answer_inline_query(update.inline_query.id, [])
