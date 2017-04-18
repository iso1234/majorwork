# The API that will be used to interface with the database
import sqlite3

connection = sqlite3.connect("main.db")
cursor = connection.cursor()
try:
    # Perform a VACUUM on the data (defragments and gets rid of supposedly empty tables that have left behind junk)
    connection.execute("VACUUM")
except Exception: # "VACUUM" doesn't work in python3.6
    pass


def confirmKey(key):
    """ Removes the record with the provided 'key' (string) in it from the 'pendingRequests' table in the DB
        and adds a new entry with the existing info (student_email and user_email) to the 'students' table """
    # Get info
    cursor.execute("SELECT * FROM pendingRequests WHERE confirmation_key=?", (key,))
    results = cursor.fetchall()
    # Delete from 'pendingRequests' DB
    cursor.execute("DELETE FROM pendingRequests WHERE confirmation_key=?", (key,))
    # Add to the 'students' DB
    addStudent(results[0][0], results[0][2])
    connection.commit()


def alreadyInPendingRequests(studentEmail, userEmail):
    """ Checks in the 'pendingRequests' table in the DB to see if that user has already sent a request to that student
    Input:
    studentEmail (str) = the email of the student being looked for in the database
    userEmail (str) = email of the user being looked for in the database
    Output:
    True (bool) = that set of data was found
    False (bool) = that set of data wasn't found """
    cursor.execute("SELECT * FROM pendingRequests WHERE student_email=? AND user_email=?", (studentEmail, userEmail))
    results = cursor.fetchall()
    if results:
        return True
    else:
        return False


def addToPendingRequests(studentEmail, confirmationKey, userEmail):
    """ Adds the given data to the 'pendingRequests' table in the DB 
    Input: all strings """
    cursor.execute("INSERT INTO pendingRequests (student_email, confirmation_key, user_email) VALUES (?, ?, ?)", (studentEmail, confirmationKey, userEmail))
    connection.commit()


def keysInUse():
    """ Returns all the keys that are in use by the 'pendingRequests' DB as a list of strings """
    cursor.execute("SELECT * FROM pendingRequests")
    results = cursor.fetchall()
    return [i[1] for i in results]


def userInDB(userEmail, userPassword):
    """ Checks in the 'users' table in the DB to see if that user exists
    Input:
    userEmail (str) = the email being looked for in the database
    userPassword (str) = the password being looked for in the database
    Output:
    True (bool) = that set of data was found
    False (bool) = that set of data wasn't found """
    cursor.execute("SELECT * FROM users WHERE user_email=? AND user_password=?", (userEmail, userPassword))
    results = cursor.fetchall()
    if results:
        return True
    else:
        return False


def getStudents(userEmail):
    """ Returns the emails of the students that belong to the provided userEmail (string) as a list of strings,
        returns False (bool) if there are no students belonging to that email """
    cursor.execute("SELECT * FROM students WHERE user_email=?", (userEmail,))
    results = cursor.fetchall()
    if results:
        return [student[0] for student in results]
    else:
        return []


def addStudent(studentEmail, userEmail):
    """ Inserts the provided information (both strings) into the 'students' table in the DB.
        Returns True (bool) if it was successful or False (bool) if that student has already been registered with that user. """
    cursor.execute("SELECT * FROM students WHERE student_email=? AND user_email=?", (studentEmail, userEmail))
    results = cursor.fetchall()
    if results:
        return False
    else:
        cursor.execute("INSERT INTO students (student_email, user_email) VALUES (?, ?)", (studentEmail, userEmail))
        connection.commit()
        return True


def insertData(userEmail, userPassword):
    """ Inserts the provided email and password (both strings) into the 'users' table in the DB.
        Returns True (bool) if it was successful or False (bool) if that email is already is use. """
    cursor.execute("SELECT * FROM users WHERE user_email=?", (userEmail,))
    results = cursor.fetchall()
    if results:
        return False
    else:
        cursor.execute("INSERT INTO users (user_email, user_password) VALUES (?, ?)", (userEmail, userPassword))
        connection.commit()
        return True


def deleteUser(userEmail, userPassword):
    """ Deletes the user corresponding to the provided email and password (both strings) from the database.
        Returns True (bool) if it was successful or False (bool) if the user doesn't exist. """
    if getUserData(email, password):
        cursor.execute("DELETE FROM users WHERE user_email=? AND user_password=?", (userEmail, userPassword))
        connection.commit()
        return True
    else:
        return False
