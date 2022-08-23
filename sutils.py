import subprocess
import platform


def get_info():
    if platform.system() == "Windows":
        return "Windows"
    if platform.system() == "Linux":
        dist_info = subprocess.check_output(["lsb_release", "-i"], text=True).lower()
        return dist_info[16:]


def get_work_env(env = "telegram, stuff or all"):
    telegram_bots = ["aiogram", "telethon", "aiohttp"]
    stuff_utils = ["bs4", "XlsxWriter", "colorama"]
    if env == "all":
            subprocess.Popen(["python3.9", "-m", "pip", "install", telegram_bots]).wait()
            subprocess.Popen(["python3.9", "-m", "pip", "install", stuff_utils]).wait()
    if env == "telegram":
        for item in telegram_bots:
            subprocess.Popen(["python3.9", "-m", "pip", "install", item]).wait()
    elif env == "stuff":
        for item in stuff_utils:
            subprocess.Popen(["python3.9", "-m", "pip", "install", item]).wait()