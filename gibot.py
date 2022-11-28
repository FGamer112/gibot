from sqlite3.dbapi2 import OperationalError
import os
import requests
import sqlite3
from pathlib import Path
import startup_utils
from UI import UI


#Prechecking, setting up, creating DB
con = sqlite3.connect("datas.db")
cur = con.cursor()
try:
    cur.execute("""CREATE TABLE saves
                    (username text, email text, api_token text)""")
    cur.execute("""INSERT INTO saves VALUES ('your username', 'your email', 'api')""")
    con.commit()
except(OperationalError):
    pass
#--------------------------------------------------

#Starting
repos = []
#-------------------------------------------------

#Main vars
NEW_REPO_NAME = ""
name_of_folder = ""
#--------------------------------------------------

#Refreshing data
def refresh(item = "user, email or api"):
    if item == "user":
        return str(cur.execute("""SELECT username FROM saves""").fetchall()[0][0])
    elif item == "email":
        return str(cur.execute("""SELECT email FROM saves""").fetchall()[0][0])
    elif item == "api":
        return str(cur.execute("""SELECT api_token FROM saves""").fetchall()[0][0])
    user_from_db = str(cur.execute("""SELECT username FROM saves""").fetchall()[0][0])
    email_from_db = str(cur.execute("""SELECT email FROM saves""").fetchall()[0][0])
    os.system(f"git config --global user.name {user_from_db}")
    os.system(f"git config --global user.email {email_from_db}")
    os.system("clear")
def global_config():
    user_from_db = str(cur.execute("""SELECT username FROM saves""").fetchall()[0][0])
    email_from_db = str(cur.execute("""SELECT email FROM saves""").fetchall()[0][0])
    os.system(f"git config --global user.name {user_from_db}")
    os.system(f"git config --global user.email {email_from_db}")
    os.system("clear")
global_config()
#--------------------------------------------------

#Path and folders
path = Path(os.path.abspath(os.path.dirname(__file__))).parent
path_alt = os.path.abspath(os.path.dirname(__file__))
content = os.listdir(str(f'{path}/'))
#--------------------------------------------------


#Starting
def start():
    os.system("clear")
    result = UI.menu("list", "start", "", ["Local", "Github", "Settings"])
    if result == "Settings":
        settings()
    elif result == "Github":
        github()
    else:
        local()

#Parsing from Github and uploading
def github():
    user_from_db = refresh("user")
    api_from_db = refresh("api")
    python_cmd = startup_utils.Python.get_python_version("str")
    headers = {
                    "Authorization": f"token {api_from_db}"
            }
    response = requests.get('https://api.github.com/user/repos', headers=headers).json()
    for dict in response:
        repos.append(dict["name"])
    repos.sort(key=str)
    repos.append(UI.separator())
    repos.append("Back")
    result = UI.menu("list", "start", "Choose your repo", repos)
    name_of_folder = result
    if result == "Back" or result == "Backspace":
        start()
    else:
        os.system("clear")
        result = UI.confirming(result, "repo")
        if result == True:
            if os.path.exists(f"{path}/{name_of_folder}"):
                result = UI.confirming("Folder exists, replace with remote?", "replace")
                if result == True:
                    os.system(f"rm -rf {path}/{name_of_folder}")
                    print("CLONING...")
                    os.system(f"cd {path} && git clone https://{user_from_db}:{api_from_db}@github.com/{user_from_db}/{name_of_folder}")
                    UI.confirming("Launch?", "launch")
                    if result == True:
                            os.system(f"cd {path}/{name_of_folder} && {python_cmd} {name_of_folder}.py")
            else:
                print("CLONING...")
                os.system(f"cd {path}/ && git clone https://{user_from_db}:{api_from_db}@github.com/{user_from_db}/{name_of_folder}")
                result = UI.confirming("Launch?", "launch")
                if result == True:
                    os.system(f"cd {path}/{name_of_folder} && {python_cmd} {name_of_folder}.py")


#MAIN MODULE folders parsing and choosing
def local():
    user_from_db = refresh("user")
    api_from_db = refresh("api")
    contlist = []
    for i, name in enumerate(content):
        if os.path.isdir(f'{path}/'):
            contlist.append(name)
    contlist.sort(key=str)
    contlist.append(UI.separator)
    contlist.append("Back")
    result = UI.menu("list", "ch", "Choose folder", contlist)
    name_of_folder = result
    if result == "Back" or result == "Backspace":
        start()
    else: 
        os.system("clear")
        headers = {
                "Authorization": f"token {api_from_db}"
        }
        response = str(requests.get('https://api.github.com/user/repos', headers=headers).json()).count(f"{name_of_folder}")
        if response >= 1:
            result = UI.menu("list", "ch", "The repository exists", ["Refresh", "Replace with local", "Delete"])
            #OPTION refresh
            if result == "Refresh":
                message = str(input("Commit message: "))
                print("\nREFRESHING...\n")
                headers = {
                            "Authorization": f"token {api_from_db}",
    }
                data = {"name":f"{name_of_folder}"}
                response = requests.patch(f'https://api.github.com/repos/FGamer112/{name_of_folder}', headers=headers, data=data, auth=(f"{user_from_db}", f"{api_from_db}"))
                print(f"Status-code: {response.status_code}\n")
                refreshing = open("refresh.sh", "w")
                refreshing.writelines(["#!/bin/bash\n", f"cd {path}/{name_of_folder}\n", "git init\n", "git add .\n", f"git commit -m '{message}'\n", f"git push https://{user_from_db}:{api_from_db}@github.com/{user_from_db}/{name_of_folder}.git main\n"])
                refreshing.close()
                os.system(f"cd {path_alt} && chmod +x refresh.sh && ./refresh.sh && rm -rf refresh.sh")
            #--------------------------------------------------

            #OPTION Replace with local repo
            elif result == "Replace with local":
                #Deleting
                print("\nDELETING...\n")
                headers = {
                            "Authorization": f"token {api_from_db}"
                            }
                response = requests.delete(f'https://api.github.com/repos/FGamer112/{name_of_folder}', headers=headers)
                print(f"Status-code: {response.status_code}\n")
                #Uploading
                result = UI.confirming("Upload as private?", "private")
                if result == True:
                    public = "false"
                else:
                    public = "true"
                print("\nUPLOADING...\n")
                print(name_of_folder)
                headers = {
                            "Authorization": f"token {api_from_db}"
                }
                data = {"name": f"{name_of_folder}", "public": f"{public}"}
                response = requests.post('https://api.github.com/user/repos', headers=headers, json=data)
                print(f"Status-code: {response.status_code}\n")
                dwnld = open("uploading.sh", "w")
                dwnld.writelines(["#!/bin/bash\n", f"cd {path}/{name_of_folder}\n", "git init\n", "git add .\n", "git commit -m 'first commit'\n", "git branch -M main\n", f"git remote add origin https://{user_from_db}:{api_from_db}@github.com/{user_from_db}/{name_of_folder}.git\n", f"git push https://{user_from_db}:{api_from_db}@github.com/{user_from_db}/{name_of_folder}.git main\n"])
                dwnld.close()
                os.system(f"cd {path_alt} && chmod +x uploading.sh && ./uploading.sh && rm -rf uploading.sh")
            #--------------------------------------------------

            #OPTION Delete
            elif result == "Delete":
                print("\nDELETING...\n")
                headers = {
                            "Authorization": f"token {api_from_db}",
    }
                response = requests.delete(f'https://api.github.com/repos/FGamer112/{name_of_folder}', headers=headers)
                print(f"Status-code: {response.status_code}\n")
            #--------------------------------------------------
        else:
            os.system("clear")
            result = UI.confirming("Upload as private?", "private")
            if result == True:
                public = "false"
            else:
                public = "true"
            print("\nUploading\n")
            print(name_of_folder)
            headers = {
                        "Authorization": f"token {api_from_db}"
            }
            data = {"name": f"{name_of_folder}", "public": f"{public}"}
            response = requests.post('https://api.github.com/user/repos', headers=headers, json=data)
            print(f"Status-code: {response.status_code}\n")
            dwnld = open("uploading.sh", "w")
            dwnld.writelines(["#!/bin/bash\n", f"cd {path}/{name_of_folder}\n", "git init\n", "git add .\n", "git commit -m 'first commit'\n", "git branch -M main\n", f"git remote add origin https://{user_from_db}:{api_from_db}@github.com/{user_from_db}/{name_of_folder}.git\n", f"git push https://{user_from_db}:{api_from_db}@github.com/{user_from_db}/{name_of_folder}.git main\n"])
            dwnld.close()
            os.system(f"cd {path_alt} && chmod +x uploading.sh && ./uploading.sh && rm -rf uploading.sh")
#--------------------------------------------------


#Settings
def settings():
        global_config()
        os.system("clear")
        user_from_db = refresh("user")
        email_from_db = refresh("email")
        api_from_db = refresh("api")
        api_for_print = api_from_db[0:4]+("*"*32)+api_from_db[36:40]
        print(f"Username: {user_from_db}\nEmail: {email_from_db}\nApi: {api_for_print}\n")
        result = UI.menu("list", "settings", "", [
                    {'name':'Username'},
                    {'name':'Email'},
                    {'name':'API-token'},
                    {'name':'Install pip packages'},
                    {'name':'Back'}
                ])
        if result == "Username":
            user = str(input("Enter username: "))
            cur.execute(f"UPDATE saves SET username = '{user}'")
            con.commit()
            settings()
        elif result == "Email":
            email = str(input("Enter Email: "))
            cur.execute(f"UPDATE saves SET email = '{email}'")
            con.commit()
            settings()
        elif result == "API-token":
            api = str(input("Enter API-token: "))
            cur.execute(f"UPDATE saves SET api_token = '{api}'")
            con.commit()
            settings()
        elif result == "Install pip packages":
            result = UI.menu("list", "environ", "Choose your environment", [
                {"name": "All"},
                {"name": "Telegram"},
                {"name": "Stuff"},
                {"name": "Back"}
            ])
            if result == "All":
                startup_utils.Python.get_work_env("all")
                settings()
            elif result == "Telegram":
                startup_utils.Python.get_work_env("telegram")
                settings()
            elif result == "Stuff":
                startup_utils.Python.get_work_env("stuff")
                settings()
            elif result == "Back" or result == "Backspace":
                settings()
        elif result == "Back" or result == "Backspace":
            start()
#--------------------------------------------------

start()
