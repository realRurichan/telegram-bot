import platform
import sys
import psutil
from telegram import Update
import telegram
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode
from loguru import logger
from plugins.CheckMessageTimedOut import CheckTimedOut
import version
import main
import time
import subprocess


def load():
    logger.info("SystemInfo is loaded")


def get_uptime():
    start_time = main.start_time
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)

    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60

    uptime_str = f"{hours}h {minutes}m {seconds}s"
    return uptime_str


def get_git_commit_hash():
    long_commit_hash = ""
    try:
        commit_hash = (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("utf-8")
            .strip()
        )
        long_commit_hash = (
            subprocess.check_output(["git", "rev-parse", "HEAD"])
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError:
        commit_hash = "unknown"
    result = {
        "commit_hash": commit_hash,
        "github_link": f"https://github.com/realRurichan/telegram-bot/commit/{long_commit_hash}",
    }
    return result


def get_version_code():
    if version.status == "git" and get_git_commit_hash()["commit_hash"] != "unknown":
        version_code = f"{version.version}+git.<a href=\"{get_git_commit_hash()['github_link']}\">{get_git_commit_hash()['commit_hash']}</a>*{version.code}"
    elif version.status == "git":
        version_code = f"{version.version}+git*{version.code}"
    else:
        version_code = f"{version.version}*{version.code}"
    return version_code


async def systeminfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CheckTimedOut(update, context):
        return
    logger.debug(str(update.to_dict()))

    os_info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
    }
    python_version = sys.version
    version_info = {
        "full_version_code": get_version_code(),
        "version": version.version,
        "code": version.code,
        "status": version.status,
    }
    ptb_version = {
        "version": telegram.__version__,
        "bot_api_version": telegram.__bot_api_version__,
    }
    hardware_info = {
        "cpu_cores": psutil.cpu_count(),
        "mem_total": psutil.virtual_memory().total,
    }
    uptime = get_uptime()

    info = (
        "<b>System Info</b>\n"
        "System:\n"
        f'system: <code>{os_info["system"]}</code>\n'
        f'release: <code>{os_info["release"]}</code>\n'
        f'version: <code>{os_info["version"]}</code>\n\n'
        "Runtime:\n"
        f"python version: <code>{python_version}</code>\n\n"
        "Core Version:\n"
        f'full version code: {version_info["full_version_code"]}\n'
        f'version: <code>{version_info["version"]}</code>\n'
        f'code: <code>{version_info["code"]}</code>\n'
        f'status: <code>{version_info["status"]}</code>\n\n'
        "Python-Telegram-Bot Version:\n"
        f'ptb version: <code>{ptb_version["version"]}</code>\n'
        f'bot api version: <code>{ptb_version["bot_api_version"]}</code>\n\n'
        "Hardware:\n"
        f'cpu cores: <code>{hardware_info["cpu_cores"]}</code>\n'
        f'mem total: <code>{hardware_info["mem_total"]}</code>\n\n'
        "Uptime:\n"
        f"uptime: {uptime}"
    )

    await update.message.reply_text(
        info, parse_mode=ParseMode.HTML, disable_web_page_preview=True
    )


handlers = [CommandHandler("systeminfo", systeminfo)]
