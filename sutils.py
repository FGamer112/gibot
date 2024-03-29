import subprocess
import platform


def get_info():
    if platform.system() == "Windows":
        return "Windows"
    if platform.system() == "Linux":
        return str(subprocess.check_output(["lsb_release", "-i"]).decode("utf-8").lower()[16:])

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

def get_installed_python3():
    versions = []
    i = 5
    while i <=10:
        try:
            subprocess.Popen([f"python3.{i}", "-V"]).wait()
            versions.append(f"python3.{i}")
            i+=1
        except:
            pass
            i+=1
    return versions

def universal_import(value):
    if type(value) is str:
        for item in get_installed_python3():
            print(item)
            subprocess.Popen([item, "-m", "pip", "install", value]).wait()
    elif type(value) is list:
        for item in get_installed_python3():
            for item1 in value:
                subprocess.Popen([item, "-m", "pip", "install", item1]).wait()

def get_work_env(env: str):
    """
    all

    telegram

    stuff

    django
    """
    telegram_bots = ["aiogram", "telethon", "aiohttp"]
    stuff_utils = ["bs4", "XlsxWriter", "colorama"]
    if env == "all":
        for item in telegram_bots:
            subprocess.Popen(["python3", "-m", "pip", "install", item]).wait()
        for item in stuff_utils:
            subprocess.Popen(["python3", "-m", "pip", "install", item]).wait()
    if env == "telegram":
        for item in telegram_bots:
            subprocess.Popen(["python3", "-m", "pip", "install", item]).wait()
    elif env == "stuff":
        for item in stuff_utils:
            subprocess.Popen(["python3", "-m", "pip", "install", item]).wait()
    elif env == "django":
        subprocess.Popen(["python3", "-m", "pip", "install", env]).wait()
        if get_info() == "opensuse":
            subprocess.Popen(["sudo", "zypper", "-n", "install", "--force", "python3-Django"])
        else:
            print(f"Your system is not exist in script. Please, send to devs at https://t.me/X0R_Tw1nky name of your system from console. We will add your system soon!)\n\nSystem name: {get_info()}")