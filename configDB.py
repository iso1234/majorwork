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
        cur.execute("""CREATE TABLE pendingPasswordResets (
                user_email VARCHAR(60),
                confirmation_key VARCHAR(60)
            ); """)
        cur.execute("""CREATE TABLE pendingDeletedAccounts (
                user_email VARCHAR(60),
                confirmation_key VARCHAR(60)
            ); """)
        cur.execute("""CREATE TABLE studentCardIDs (
                student_email VARCHAR(60),
                card_id VARCHAR(60)
            ); """)
        cursor.execute("INSERT INTO studentCardIDs (student_email, card_id) VALUES ('coateslachlan@inaburrastudents.nsw.edu.au', '5CEF083E')")
        cursor.execute("INSERT INTO studentCardIDs (student_email, card_id) VALUES ('greeneisaac@inaburrastudents.nsw.edu.au', '6C7C413E')")
        cursor.execute("INSERT INTO studentCardIDs (student_email, card_id) VALUES ('parkharry@inaburrastudents.nsw.edu.au', 'ACFF293E')")
        cursor.execute("INSERT INTO studentCardIDs (student_email, card_id) VALUES ('feodoroffdaniel@inaburrastudents.nsw.edu.au', 'FCFA293E')")
        cursor.execute("INSERT INTO studentCardIDs (student_email, card_id) VALUES ('lynchluke@inaburrastudents.nsw.edu.au', '0C9D413E')")
        conn.commit()
        conn.close()
        print("Database created")
