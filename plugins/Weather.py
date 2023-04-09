import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
from telegram.constants import ParseMode
from loguru import logger
import requests
import json

load_dotenv()

def load():
    logger.info("Weather is loaded.")

qweather_key = os.getenv("QWEATHER_KEY")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_city = feedback_content = update.message.text[9: ]
    if target_city == '':
        await update.message.reply_text("请在后面接上想要查询的城市w")
        return
    geoapi = requests.get(f'https://geoapi.qweather.com/v2/city/lookup?key={qweather_key}&location={target_city}&lang=zh')
    geoapi_result = geoapi.json()
    if (geoapi_result['code'] != '200'):
        await update.message.reply_text("小兔子查询不到你想要查询的城市哦，请检查后再试试qwq")
        return
    location = geoapi_result["location"][0]
    location_id = location['id']
    weather_api = requests.get(f'https://devapi.qweather.com/v7/weather/now?key={qweather_key}&location={location_id}&lang=zh')
    weather_api_result = weather_api.json()
    weather_info = weather_api_result["now"]
    if location["name"] != location["adm2"]:
        city_name = location["adm2"] + location["name"]
    else:
        city_name = location["name"]
    try:
        air_quality_api = requests.get(f'https://devapi.qweather.com/v7/air/now?key={qweather_key}&location={location_id}&lang=zh')
        air_quality_api_result = air_quality_api.json()
        air_quality_info = air_quality_api_result["now"]
        await update.message.reply_text(f"{city_name} 的天气为：\n"
                                        f"{weather_info['text']} {weather_info['temp']}°C\n"
                                        f"{weather_info['windDir']} {weather_info['windScale']} 级\n"
                                        f"空气质量 {air_quality_info['category']} AQI {air_quality_info['aqi']}")
        return
    except:
        await update.message.reply_text(f"{city_name} 的天气为：\n"
                                        f"{weather_info['text']} {weather_info['temp']}°C\n"
                                        f"{weather_info['windDir']} {weather_info['windScale']} 级\n")
        return

handlers = [CommandHandler(['weather'], weather)]


    