from dotenv import load_dotenv
from loguru import logger
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Updater
import plugins as bot_plugins
import os
import time

load_dotenv()

start_time = time.time()

'''
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
'''

def main():
    application = ApplicationBuilder().token(os.getenv("BOTTOKEN")).build()
    for plugin in bot_plugins.__all__:
        plugin.load()
        for handler in plugin.handlers:
                application.add_handler(handler)
    application.add_error_handler(bot_plugins.ErrorHandler.error_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == '__main__':
    main()