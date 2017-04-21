import os
import sqlite3

def createDB():
    if os.path.exists("studentTimes.db"):
        print("Already exists")
    else:
        conn = sqlite3.connect("studentTimes.db")
        cur = conn.cursor()
        cur.execute("""CREATE TABLE cardTimes (
                card_id VARCHAR(45),
                time VARCHAR(45)
            ); """)

        conn.commit()
        conn.close()
        print("Database created")
