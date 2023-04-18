import os
from dotenv import load_dotenv
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, InlineQueryHandler
from loguru import logger
from pixivpy_async import PixivClient, AppPixivAPI
import re

load_dotenv()

regex = r'https?://(?:www\.)?pixiv\.net/(?:\w+/)?artworks/(\d+)'
def match(query= str):
    result = re.match(regex, query)
    if(result):
        logger.debug(f'Matched')
    return result

def load():
    logger.info("Pixiv Inline Share is loaded.")

async def main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    match = re.search(regex, query)

    if match:
        illustration_id = int(match.group(1))
        pixiv_refreshtoken = os.getenv("PIXIV_REFRESHTOKEN")
        async with PixivClient() as client:
            api = AppPixivAPI(client=client)
            await api.login(refresh_token=pixiv_refreshtoken)
            try:
                illustration = await api.illust_detail(illustration_id)
                image_url = illustration.illust.image_urls.large
            except(AttributeError):
                await context.bot.answer_inline_query(update.inline_query.id, [])
                return

            # Thanks for pixiv.cat
            proxy_image_url = image_url.replace("https://i.pximg.net", "https://i.pixiv.cat")

            results = [
            InlineQueryResultArticle(
                id=illustration_id,
                title=illustration.illust.title,
                description=f"By {illustration.illust.user.name}",
                input_message_content=InputTextMessageContent(
                    message_text=(
                                f"Pixiv Share\n"
                                f"[{illustration.illust.title}]({proxy_image_url}) by {illustration.illust.user.name}\n"
                                f"[Original link]({query})"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                ),
                thumb_url=proxy_image_url
            )
            ]
            
            logger.debug(results)
            await context.bot.answer_inline_query(update.inline_query.id, results)
        

    else:
        await context.bot.answer_inline_query(update.inline_query.id, [])

# handlers = [InlineQueryHandler(pixiv_inline_share, pattern=regex)]
