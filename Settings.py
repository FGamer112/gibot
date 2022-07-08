import sqlite3
from pathlib import Path

class settings():
    def starting_settings():
            con = sqlite3.Connection("Settings.db")
            cur = con.cursor()
            cur.execute("""CREATE TABLE settings (
username text,
email text,
token text
working_directory text,
db_backup bool
)""")
            cur.execute(f"""INSERT INTO settings VALUES (
'your username',
'your email',
'your token',
'{Path.cwd()}',
'{False}')""")
            con.commit()

    def get_current_settings():
        con = sqlite3.Connection("Settings.db")
        cur = con.cursor()
        answer = cur.execute("SELECT * FROM settings").fetchall()
        print(answer)
settings.starting_settings()
settings.get_current_settings()