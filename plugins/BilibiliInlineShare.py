from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes, InlineQueryHandler
from telegram.constants import ParseMode
from loguru import logger
import re

def load():
    logger.info("BilibiliShare module is loaded")

async def bilibili_share(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    pattern = r"(?i)(av\d+|BV[\dA-Za-z]{10})"
    match = re.match(pattern, query)

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
        
handlers = [InlineQueryHandler(bilibili_share, pattern=r"(?i)(av\d+|BV[\dA-Za-z]{10})")]

