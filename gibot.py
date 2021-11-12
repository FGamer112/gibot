from sqlite3.dbapi2 import OperationalError
from PyInquirer import prompt, Separator
import os
import requests
import sqlite3


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

#DB
user_from_db = str(cur.execute("""SELECT username FROM saves""").fetchall()[0][0])
email_from_db = str(cur.execute("""SELECT email FROM saves""").fetchall()[0][0])
api_from_db = str(cur.execute("""SELECT api_token FROM saves""").fetchall()[0][0])

#Starting
repos = []
#--------------------------------------------------

#Main vars
NEW_REPO_NAME = ""
name_of_folder = ""
result = ""
def menu(type_of, name, message, choises):
    questions = [{
        "type": f"{type_of}",
        "name": f"{name}",
        "message": f"{message}",
        "choices": choises
    }]
    global result
    result = prompt(questions)[f"{name}"]

def confirming(message, name):
    questions = [
    {
        'type': 'confirm',
        'message': message,
        'name': f'{name}',
        'default': True,
    }
]
    global result
    result = prompt(questions)[f"{name}"]
#--------------------------------------------------

#Path and folders
path = os.path.abspath(os.path.dirname(__file__))
content = os.listdir(str(path+"/"))
contlist = []
#--------------------------------------------------


os.system(f"git config --global user.name {user_from_db}")
os.system(f"git config --global user.email {email_from_db}")
os.system("clear")


#Starting
def start():
    os.system("clear")
    menu("list", "start", "", ["Local", "Github", "Settings"])
    if result == "Settings":
        settings()
    elif result == "Github":
        github()
    else:
        local()

#Parsing from Github and uploading
def github():
    os.system("clear")
    repos = []
    headers = {
                    "Authorization": f"token {api_from_db}"
            }
    response = requests.get('https://api.github.com/user/repos', headers=headers).json()
    for dict in response:
        repos.append(dict["name"])
    repos.sort(key=str)
    repos.append(Separator())
    repos.append("Back")
    menu("list", "start", "Choose your repo", repos)
    global name_of_folder
    name_of_folder = result
    if result == "Back":
        start()
    else:
        os.system("clear")
        confirming(result, "repo")
        if result == True:
            contlist = []
            for i, name in enumerate(content):
                if os.path.isdir(path+"/"+name):
                    contlist.append(name)
            contlist.sort(key=str)
            try:
                folder_exist_checking = contlist.index(f"{name_of_folder}")
                if folder_exist_checking >= 0:
                    confirming("Folder exists, replace with remote?", "replace")
                    if result == True:
                        import random
                        salt = random.randint(1000000, 9999999)
                        os.system(f"cd {path}/ && mkdir temp{salt}")
                        os.system(f"rm -rf {name_of_folder}")
                        print("CLONING...")
                        os.system(f"cd {path}/temp{salt} && git clone https://{user_from_db}:{api_from_db}@github.com/{user_from_db}/{name_of_folder}")
                        os.system(f"\cp -r {path}/temp{salt}/{name_of_folder} {path}/ && rm -rf {path}/temp{salt}")
                        confirming("Launch?", "launch")
                        if result == True:
                                os.system(f"cd {path}/{name_of_folder} && python3 {name_of_folder}.py")
            except(ValueError):
                print("CLONING...")
                os.system(f"cd {path}/ && git clone https://{user_from_db}:{api_from_db}@github.com/{user_from_db}/{name_of_folder}")
                confirming("Launch?", "launch")
                if result == True:
                        os.system(f"cd {path}/{name_of_folder} && python3 {name_of_folder}.py")


#MAIN MODULE folders parsing and choosing
def local():
    contlist = []
    for i, name in enumerate(content):
        if os.path.isdir(path+"/"+name):
            contlist.append(name)
    contlist.sort(key=str)
    contlist.append(Separator())
    contlist.append("Back")
    menu("list", "ch", "Choose folder", contlist)
    global name_of_folder
    name_of_folder = result
    if result == "Back":
        start()
    else: 
        os.system("clear")
        headers = {
                "Authorization": f"token {api_from_db}"
        }
        response = str(requests.get('https://api.github.com/user/repos', headers=headers).json()).count(f"{name_of_folder}")
        if response >= 1:
            menu("list", "ch", "The repository exists", ["Refresh", "Replace with local", "Delete"])
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
                os.system(f"cd {path} && chmod +x refresh.sh && ./refresh.sh && rm -rf refresh.sh")
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
                confirming("Upload as private?", "private")
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
                os.system(f"cd {path} && chmod +x uploading.sh && ./uploading.sh && rm -rf uploading.sh")
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
            confirming("Upload as private?", "private")
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
            os.system(f"cd {path} && chmod +x uploading.sh && ./uploading.sh && rm -rf uploading.sh")
#--------------------------------------------------


#Settings
def settings():
        os.system("clear")
        global user_from_db
        global email_from_db
        global api_from_db
        user_from_db = str(cur.execute("""SELECT username FROM saves""").fetchall()[0][0])
        email_from_db = str(cur.execute("""SELECT email FROM saves""").fetchall()[0][0])
        api_for_print = api_from_db[0:4]+("*"*32)+api_from_db[36:40]
        print(f"Username: {user_from_db}\nEmail: {email_from_db}\nApi: {api_for_print}\n")
        menu("list", "settings", "", [
                    {'name':'Username'},
                    {'name':'Email'},
                    {'name':'API-token'},
                    {'name':'Back'}
                ])
        if result == "Username":
            user = str(input("Enter username: "))
            cur.execute(f"UPDATE saves SET username = '{user}'")
            con.commit()
            user_from_db = user
            settings()
        elif result == "Email":
            email = str(input("Enter Email: "))
            cur.execute(f"UPDATE saves SET email = '{email}'")
            con.commit()
            email_from_db = email
            settings()
        elif result == "API-token":
            api = str(input("Enter API-token: "))
            cur.execute(f"UPDATE saves SET api_token = '{api}'")
            con.commit()
            api_from_db = api
            settings()
        elif result == "Back":
            start()
#--------------------------------------------------

start()
