import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from loguru import logger
import aiohttp
from plugins.CheckMessageTimedOut import CheckTimedOut

load_dotenv()


def load():
    logger.info("Weather is loaded.")


qweather_key = os.getenv("QWEATHER_KEY")
amap_key = os.getenv("AMAP_KEY")


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CheckTimedOut(update, context):
        return
    logger.debug(str(update.to_dict()))
    status_amap = False
    target_loc = update.message.text[9:]
    if target_loc == "":
        await update.message.reply_text("请在后面接上想要查询的城市w")
        return
    geoapi = await fetch(
        f"https://geoapi.qweather.com/v2/city/lookup?key={qweather_key}&lang=zh&location={target_loc}"
    )
    geoapi_result = geoapi.json()
    if geoapi_result["code"] != "200":
        poiapi = await fetch(
            f"https://geoapi.qweather.com/v2/poi/lookup?key={qweather_key}&type=scenic&lang=zh&location={target_loc}"
        )
        poiapi_result = poiapi.json()
        if poiapi_result["code"] != "200":
            status_amap = True
            amap_api = await fetch(
                f"https://restapi.amap.com/v3/geocode/geo?key={amap_key}&address={target_loc}"
            )
            amap_api_result = amap_api.json()
            if amap_api_result["status"] == "0":
                await update.message.reply_text("小兔子查询不到你想要查询的城市哦，请检查后再试试qwq")
                return
            else:
                location_amap = amap_api_result["geocodes"][0]

    if status_amap == False:
        try:
            location = geoapi_result["location"][0]
        except:
            location = poiapi_result["poi"][0]
        lon = location["lon"]
        lat = location["lat"]
        lon_lat = f"{location['lon']},{location['lat']}"
        if (location["name"] != location["adm2"]) and geoapi_result["code"] == "200":
            city_name = location["adm2"] + location["name"]
        else:
            city_name = location["name"]
    else:
        lon_lat = location_amap["location"]
        city_name = location_amap["formatted_address"]
    weather_api = await fetch(
        f"https://devapi.qweather.com/v7/grid-weather/now?key={qweather_key}&lang=zh&location={lon_lat}"
    )
    weather_api_result = weather_api.json()
    logger.debug(f"Weather Info: {weather_api_result}")
    weather_info = weather_api_result["now"]
    try:
        air_quality_api = await fetch(
            f"https://devapi.qweather.com/v7/air/now?key={qweather_key}&lang=zh&location={lon_lat}"
        )
        air_quality_api_result = air_quality_api.json()
        air_quality_info = air_quality_api_result["now"]
        await update.message.reply_text(
            f"{city_name} 的天气为：\n"
            f"{weather_info['text']} {weather_info['temp']}°C\n"
            f"{weather_info['windDir']} {weather_info['windScale']} 级\n"
            f"空气质量 {air_quality_info['category']} AQI {air_quality_info['aqi']}\n"
            f"小兔子祝你一天好心情哦~"
        )
        return
    except:
        await update.message.reply_text(
            f"{city_name} 的天气为：\n"
            f"{weather_info['text']} {weather_info['temp']}°C\n"
            f"{weather_info['windDir']} {weather_info['windScale']} 级\n"
            f"小兔子祝你一天好心情哦~"
        )
        return


handlers = [CommandHandler(["weather"], weather)]
