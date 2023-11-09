import sqlite3
from datetime import datetime

global database_nm 
database_nm = "travel_data_new.db" #check this file in sql lite studio to query data

def get_all_states():
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    query = f"select distinct state from location;"
    all_locations = cur.execute(query).fetchall()
    print(all_locations)
    return [location[0] for location in all_locations]   
    
def find_user_login(username):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    sql_query = f"SELECT distinct password FROM users where username = '{username}';"
    t = cur.execute(sql_query).fetchall()
    return str("".join(t[0]))
    
def select_all_from_table(table_name, where_clause):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    if where_clause is not None:
        query = f"select * from {table_name} where " + where_clause
    else:
        query = f"select * from {table_name}"
    print(query)
    all_users = cur.execute(query).fetchall()
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

def insert_or_update_location(state, name, description, locationcategory, image_url):
    connection = sqlite3.connect(database_nm)
    cur = connection.cursor()
    cur.execute("INSERT INTO location (state, name, description,locationcategory, image_url) VALUES (?, ?, ?, ?, ?)",
                    (state, name, description, locationcategory, image_url))
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