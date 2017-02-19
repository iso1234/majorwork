# The api that will be used to interface with the database
import sqlite3

connection = sqlite3.connect("users.db")
cursor = connection.cursor()
try:
    # Perform a VACUUM on the data (defragments and gets rid of supposedly empty tables that have left behind junk)
    connection.execute("VACUUM")
except Exception: # "VACUUM" doesn't work in python3.6
    pass


def getUserData(email, password):
    """ Retrieves user data if the email and password are a valid user in the database.
        Returns the users info or False. """
    cursor.execute("SELECT * FROM users WHERE user_email=? AND user_password=?", (email, password))
    results = cursor.fetchall()
    if results:
        uid, email, *_ = results[0]
        return {"uid": uid, "email": email}
    else:
        return False


def getStudents(uid):
    """ Returns the students that belong to the provided id,
        returns false if there are no students belonging to that id """
    cursor.execute("SELECT * FROM students WHERE parent_id=?", (uid,))
    results = cursor.fetchall()
    if results:
        return {student[1]: student[2] for student in results}
    else:
        return {}
    


def insertData(email, password):
    """ Inserts the provided email and password into the database.
        Returns True if it was successful or False if that username is already is use. """
    cursor.execute("SELECT * FROM users WHERE user_email=?", (email,))
    results = cursor.fetchall()
    if results:
        return False
    else:
        cursor.execute("INSERT INTO users (user_email, user_password) VALUES (?, ?)", (email, password))
        connection.commit()
        return True


def deleteUser(email, password):
    """ Deletes the user corresponding to the provided email and password from the database.
        Returns True if it was successful or False if the user doesn't exist. """
    if getUserData(email, password):
        cursor.execute("DELETE FROM users WHERE user_email=? AND user_password=?", (email, password))
        connection.commit()
        return True
    else:
        return False
