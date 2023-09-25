import sqlite3
from datetime import datetime

global database_nm 
database_nm = "travel_db.db" #check this file in sql lite studio to query data

def find_user_login(username):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    sql_query = f"SELECT distinct password FROM users where username = '{username}';"
    t = cur.execute(sql_query).fetchall()
    return str("".join(t[0]))
    
def select_all_users():
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    all_users = cur.execute("select * from users").fetchall()
    return [user for user in all_users]

def create_table():
   connection = sqlite3.connect(database_nm) 
   with open('schema.sql') as f:
        connection.executescript(f.read())
    
def insert_query_user(username, email, password, fname, lname):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cur.execute("INSERT INTO users (username, email, password, firstname, lastname) VALUES (?, ?, ?, ?, ?)",
                    (username, email, password, fname, lname))
    connection.commit()
    return "Record Inserted Successfully"

def update_user_new_login(username):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    sql_statement = f"INSERT INTO user_sessions(username,logout_time) VALUES('{username}','')";  
    cur.execute(sql_statement)
    connection.commit()

def log_user_session(username, session_id):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    sql_statement = f"UPDATE user_sessions SET logout_time = CURRENT_TIMESTAMP, session_id = '{session_id}' WHERE username='{username}' and session_id is NULL"   
    cur.execute(sql_statement)
    connection.commit()
    connection.close()