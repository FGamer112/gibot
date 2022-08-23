import subprocess
import platform


def get_info():
    if platform.system() == "Windows":
        return "Windows"
    if platform.system() == "Linux":
        return subprocess.check_output(["lsb_release", "-i"], text=True).lower()[16:]

def get_python_version(result: str):
    """
    If you want to get result as string, type "str" as arg,
    for float type "float"
    """
    res = subprocess.check_output(["python3", "-V"]).decode()[7:]
    if result == "str":
        return res.split(".")[0]+"."+res.split(".")[1]
    else:
        return float(res.split(".")[0]+"."+res.split(".")[1])


def get_work_env(env: str):
    """
    all

    telegram

    stuff
    """
    telegram_bots = ["aiogram", "telethon", "aiohttp"]
    stuff_utils = ["bs4", "XlsxWriter", "colorama"]
    if env == "all":
        for item in telegram_bots:
            subprocess.Popen(["python3.9", "-m", "pip", "install", item]).wait()
        for item in stuff_utils:
            subprocess.Popen(["python3.9", "-m", "pip", "install", item]).wait()
    if env == "telegram":
        for item in telegram_bots:
            subprocess.Popen(["python3.9", "-m", "pip", "install", item]).wait()
    elif env == "stuff":
        for item in stuff_utils:
            subprocess.Popen(["python3.9", "-m", "pip", "install", item]).wait()