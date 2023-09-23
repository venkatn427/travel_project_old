import sqlite3
from datetime import datetime 
from init_db import database_nm, create_table

def log_user_session(username, session_id, logout_time, user_session=False):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    if user_session:
        logout_time = str(datetime.now())
        
    cur.execute("INSERT INTO user_sessions(username, session_id, logout_time) VALUES (?, ?, ?)",
                    (username, session_id, logout_time))
    connection.commit()
    connection.close()
    print("Record Inserted Successfully")


create_table()

username = "ruchi"
session_id = "2649234827"
user_session = True
logout_time = ""
log_user_session(username, session_id, logout_time, user_session)
