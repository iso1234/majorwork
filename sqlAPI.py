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
        Used when a user first logs-in.
        Returns the users info or False. """
    cursor.execute("SELECT * FROM users WHERE user_email=? AND user_password=?", (email, password))
    results = cursor.fetchall()
    if results:
        uid, email, *_ = results[0]
        return {"uid": uid, "email": email}
    else:
        return False


def getStudents(parentID):
    """ Returns the emails of the students that belong to the provided id,
        returns false if there are no students belonging to that id """
    cursor.execute("SELECT * FROM students WHERE parent_id=?", (parentID,))
    results = cursor.fetchall()
    if results:
        return [student[0] for student in results]
    else:
        return []


def addStudent(studentEmail, parentID):
    """ Inserts the provided information into the `students` table in the database.
        Returns True if it was successful or False if that student has already been registered with that parent_id. """
    cursor.execute("SELECT * FROM students WHERE student_email=? AND parent_id=?", (studentEmail, parentID))
    results = cursor.fetchall()
    if results:
        return False
    else:
        cursor.execute("INSERT INTO students (student_email, parent_id) VALUES (?, ?)", (studentEmail, parentID))
        connection.commit()
        return True


def insertData(email, password):
    """ Inserts the provided email and password into the `users` table in the database.
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
