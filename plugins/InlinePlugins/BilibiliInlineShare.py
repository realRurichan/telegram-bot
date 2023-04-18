from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from loguru import logger
import re

regex = r"(?i)(av\d+|BV[\dA-Za-z]{10})"
def match(query: str):
    result = re.match(regex, query)
    if(result):
        logger.debug(f'Matched')
    return result

async def main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    match = re.match(regex, query)

    if match:
        video_id = match.group(1)
        video_url = f"https://www.bilibili.com/video/{video_id}"
        results = [
            InlineQueryResultArticle(
                id='1',
                title="Share Bilibili Video",
                input_message_content=InputTextMessageContent(
                    message_text=f"<a href='{video_url}'>{video_id}</a>",
                    parse_mode=ParseMode.HTML
                ),
                description=video_url,
                thumb_url='https://s1.hdslb.com/bfs/static/jinkela/space/assets/playlistbg.png'
            )
        ]
        await context.bot.answer_inline_query(update.inline_query.id, results)
    else:
        await context.bot.answer_inline_query(update.inline_query.id, [])

