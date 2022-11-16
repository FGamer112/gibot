import subprocess
import platform
import os
from pathlib import Path
import os


def derby(item):
    file = open("test.txt", "w")
    file.write(str(item))
    file.close()
def derby_append(item):
    file = open("test.txt", "a")
    file.write(str(item))
    file.close()


#SYSTEM
class System:
    def get_info():
        if platform.system() == "Windows":
            return "Windows"
        if platform.system() == "Linux":
            return subprocess.check_output(["lsb_release", "-i"], text=True).lower()[16:]
#----------------------------------------------------------------------------------------------------


#PYTHON
class Python:
    def get_python_version(result = "str"):
        """
        If you want to get result as string, type "str" as arg,
        for float type "float"
        Result: Python3.X.X
        """
        res = subprocess.check_output(["python3", "-V"]).decode()[7:]
        if result == "str":
            return res.split(".")[0]+"."+res.split(".")[1]
        else:
            return float(res.split(".")[0]+"."+res.split(".")[1])


    def get_installed_python3():
        versions = []
        i = 5
        while i <=11:
            try:
                subprocess.check_output([f"python3.{i}","-V" ])
                versions.append(f"python3.{i}")
                i+=1
                # print (versions)
            except:
                i+=1
        return versions


    def get_work_env(env: str):
        """
        all

        telegram

        stuff
        """
        telegram_bots = ["aiogram", "telethon", "aiohttp"]
        stuff_utils = ["bs4", "XlsxWriter", "colorama"]
        vers = []
        for item in Python.get_installed_python3():
            vers.append(item)
        if env == "all":
            for item in telegram_bots:
                for item1 in vers:
                    subprocess.Popen([item1, "-m", "pip", "install", item]).wait()
            for item in stuff_utils:
                for item1 in vers:
                    subprocess.Popen([item1, "-m", "pip", "install", item]).wait()
        if env == "telegram":
            for item in telegram_bots:
                for item1 in vers:
                    subprocess.Popen([item1, "-m", "pip", "install", item]).wait()
        elif env == "stuff":
            for item in stuff_utils:
                for item1 in vers:
                    subprocess.Popen([item1, "-m", "pip", "install", item]).wait()
    

    def searching(cwd, which = "'files' or 'modules'", names = ("__pycache__", ".git"), ext = [".py"]):
        files = []
        modules = []
        for dirpath, _, filenames in os.walk(cwd):
            if not any(dirpath.__contains__(x) for x in names):
                for filename in filenames:
                    if any(filename.endswith(x) for x in ext):
                        files.append(f"{dirpath}/{filename}")
        for item in files:
            file = open(item, "r").readlines()
            for item1 in file:
                if item1.startswith("import "):
                    try:
                        modules.index(item1.replace("import ", "").replace("\n", ""))
                    except ValueError:
                        modules.append(item1.replace("import ", "").replace("\n", ""))
        if which == "files":
            return files
        elif which == "modules":
            return modules
    

    def installing_depends(modules):
        checking = str(subprocess.run(("python3", "-m", "pip", "list")))
        for item in modules:
            if not checking.__contains__(item):
                subprocess.run(("python3", "-m", "pip", "install", f"{item}"))
#----------------------------------------------------------------------------------------------------

#DATABASE
# class Database:
#     def db_checking(folder = None):
#         result = []
#         if folder == None:
#             folder = Path.cwd().parent
#         for item in os.scandir(folder):
#             for item1 in os.scandir(item):
#                 if item1.name.__contains__(".db"):
#                     print(f"""
# NAME:  {item1.name}  PATH: {item1.path}
# """)
#                     result.append({"name": f"{item1.name}", "path": f"{item1.path}"})
#         return result

#     def db_backup():
#         menu = ["All of them"]
#         menu.append(UI.separator)
#         menu.append(Database.db_checking())
#         menu.append(UI.separator)
#         menu.append("Back")
#         UI.menu(message="Which one of options?", choises=menu)
# Database.db_backup()