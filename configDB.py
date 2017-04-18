import os
import sqlite3

def createDB():
    """ If the database 'main.db' doesn't already exist, create it. """
    if os.path.exists("main.db"):
        print("The database 'main.db' already exists.")
    else:
        conn = sqlite3.connect("main.db")
        cur = conn.cursor()
        cur.execute("""CREATE TABLE users (
                user_email VARCHAR(60),
                user_password VARCHAR(45)
            ); """)
        cur.execute("""CREATE TABLE students (
                student_email VARCHAR(60),
                user_email VARCHAR(60)
            ); """)
        cur.execute("""CREATE TABLE pendingStudentRequests (
                student_email VARCHAR(60),
                confirmation_key VARCHAR(60),
                user_email VARCHAR(60)
            ); """)
        cur.execute("""CREATE TABLE pendingAccounts (
                user_email VARCHAR(60),
                confirmation_key VARCHAR(60),
                user_password VARCHAR(60)
            ); """)
        conn.commit()
        conn.close()
        print("Database created")
