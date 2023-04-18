from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from loguru import logger
from plugins.CheckMessageTimedOut import CheckTimedOut


def load():
    logger.info("UsagePlugin is loaded.")


async def usage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CheckTimedOut(update, context):
        return
    logger.debug(str(update.to_dict()))
    await update.message.reply_text(
        f'你好，我是月兔！是<a href="tg://user?id=1603449979">琉璃</a>家的一只小兔子\n'
        f"下面来介绍我的使用方式哦\n"
        f"首先，你可以使用 <code>/hello</code> 或者是 <code>/hi</code> 来和我打招呼，我会回复你w\n"
        f"当你首次在私聊中和我说话的时候，我也会向你打招呼的！\n"
        f"当你难过的时候可以使用 <code>/hug</code> 指令，月兔会抱抱你的qwq\n"
        f"然后呢，你可以使用 <code>/getid</code> 和 <code>/userinfo</code> 来让我获取你的用户ID和用户信息w\n"
        f"还可以通过 <code>/enable</code> 和 <code>/disable</code> 可以启用和禁用月兔的一些功能哦\n"
        f"目前可以启用禁用的功能只有进群欢迎（welcome）呢QAQ，小兔子会加油学习的qwq\n"
        f"如果对小兔子有什么建议的话，可以使用 <code>/feedback &lt;content&gt;</code> 来向小兔子的妈妈反馈哦\n"
        f"最后的最后，如果你喜欢我的话，可以用 <code>/feed</code> 喂我一根胡萝卜哦，你也可以送别人的说！（虽然不知道别人爱不爱吃呢...）\n"
        f"大家请多关照w",
        parse_mode="HTML",
    )


handlers = [CommandHandler(["usage", "help"], usage)]
