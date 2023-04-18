from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, InlineQueryHandler
from loguru import logger
import aiohttp
from telegram.ext.filters import BaseFilter
import re

def load():
    logger.info("HitokotoInline module is loaded")

regex = r'^$'
def match(query= str):
    result = re.match(regex, query)
    if(result):
        logger.debug(f'Matched')
    return result

async def get_hitokoto():
    url = "https://v1.hitokoto.cn?c=a&c=b&c=c&c=d&c=e&c=g&c=h&c=i&c=k"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
        
async def main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(str(update.to_dict()))
    hitokoto = await get_hitokoto()
    logger.debug(f"Get Hitokoto: {hitokoto}")
    if hitokoto['from_who'] != None:
        hitokoto_from = f"—{hitokoto['from_who']}「{hitokoto['from']}」"
    else:
        hitokoto_from = f"—「{hitokoto['from']}」"
    results = [
    InlineQueryResultArticle(
        id='1',
        title="Hitokoto 一言",
        description=f"{hitokoto['hitokoto']} {hitokoto_from}",
        input_message_content=InputTextMessageContent(
            message_text=(
                        f"<b>Hitokoto 一言</b>\n"
                        f"{hitokoto['hitokoto']}\n"
                        f"{hitokoto_from}\n"
                        f'<a href="https://hitokoto.cn?uuid={hitokoto["uuid"]}">Original link</a>'
            ),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        ),
    )
    ]
    await context.bot.answer_inline_query(update.inline_query.id, results, cache_time=0)
    return True
    

#handlers = [InlineQueryHandler(hitokoto_inline)]