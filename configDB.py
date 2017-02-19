import os
import sqlite3

def createDB():
    """ If the database 'users.db' doesn't already exist, create it. """
    if os.path.exists("users.db"):
        print("The database 'users.db' already exists.")
    else:
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("""CREATE TABLE users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email VARCHAR(60),
                user_password VARCHAR(45)
            ); """)
        cur.execute("""CREATE TABLE students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name VARCHAR(60),
                student_key VARCHAR(60),
                parent_id INTEGER NOT NULL
            ); """)
        conn.commit()
        conn.close()
        print("Database created")
