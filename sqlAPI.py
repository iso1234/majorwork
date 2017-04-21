# The API that will be used to interface with the database
import sqlite3

connection = sqlite3.connect("main.db")
cursor = connection.cursor()
try:
    # Perform a VACUUM on the data (defragments and gets rid of supposedly empty tables that have left behind junk)
    connection.execute("VACUUM")
except Exception: # "VACUUM" doesn't work in python3.6
    pass


##==================================================================================================================##
##===========================================  Pending Deleted Accounts  ===========================================##
##==================================================================================================================##


def confirmPendingDeletedAccount(key):
    """ Removes the record with the provided 'key' (string) in it from the 'pendingDeletedAccounts' table in the DB
        and deletes the corresponding account in the 'users' table """
    # Get info
    cursor.execute("SELECT * FROM pendingDeletedAccounts WHERE confirmation_key=?", (key,))
    results = cursor.fetchall()
    # Delete from 'pendingDeletedAccounts' table in the DB
    cursor.execute("DELETE FROM pendingDeletedAccounts WHERE confirmation_key=?", (key,))
    # Delete from 'users' table in the DB
    deleteUser(results[0][0])
    connection.commit()


def alreadyInPendingDeletedAccounts(userEmail):
    """ Checks in the 'pendingDeletedAccounts' table in the DB to see if that user has already sent a request for their account to be deleted
    Input:
    userEmail (str) = the email of the user being looked for in the database
    Output:
    True (bool) = the data was found
    False (bool) = the data wasn't found """
    cursor.execute("SELECT * FROM pendingDeletedAccounts WHERE user_email=?", (userEmail,))
    results = cursor.fetchall()
    if results:
        return True
    else:
        return False


def addToPendingDeletedAccounts(userEmail, confirmationKey):
    """ Adds the given data (all strings) to the 'pendingDeletedAccounts' table in the DB """
    cursor.execute("INSERT INTO pendingDeletedAccounts (user_email, confirmation_key) VALUES (?, ?)", (userEmail, confirmationKey))
    connection.commit()


def keysInPendingDeletedAccounts():
    """ Returns all the keys that are in use by the 'pendingDeletedAccounts' table in the DB as a list of strings """
    cursor.execute("SELECT * FROM pendingDeletedAccounts")
    results = cursor.fetchall()
    return [i[1] for i in results]


##==================================================================================================================##
##===========================================  Pending password resets  ============================================##
##==================================================================================================================##


def resetPassword(key, newPassword):
    """ Removes the record with the provided 'key' (string) in it from the 'pendingPasswordResets' table in the DB,
        deletes the old entry from the 'users' table and adds a new entry with the updated password,
        newPassword (string), to the 'users' table """
    # Get info
    cursor.execute("SELECT * FROM pendingPasswordResets WHERE confirmation_key=?", (key,))
    userEmail = cursor.fetchall()[0][0]
    # Delete from 'pendingPasswordResets' table in the DB
    cursor.execute("DELETE FROM pendingPasswordResets WHERE confirmation_key=?", (key,))
    # Delete the old entry from 'users' table
    cursor.execute("DELETE FROM users WHERE user_email=?", (userEmail,))
    # Add to the 'users' table in the DB
    addUser(userEmail, newPassword)
    connection.commit()


def alreadyInPendingPasswordResets(userEmail):
    """ Checks in the 'pendingPasswordResets' table in the DB to see if that user has already sent a confirmation email
    Input:
    userEmail (str) = the email of the user being looked for in the database
    Output:
    True (bool) = the data was found
    False (bool) = the data wasn't found """
    cursor.execute("SELECT * FROM pendingPasswordResets WHERE user_email=?", (userEmail,))
    results = cursor.fetchall()
    if results:
        return True
    else:
        return False


def addToPendingPasswordResets(userEmail, confirmationKey):
    """ Adds the given data (all strings) to the 'pendingAccounts' table in the DB """
    cursor.execute("INSERT INTO pendingPasswordResets (user_email, confirmation_key) VALUES (?, ?)", (userEmail, confirmationKey))
    connection.commit()


def keysInPendingPasswordResets():
    """ Returns all the keys that are in use by the 'pendingPasswordResets' table in the DB as a list of strings """
    cursor.execute("SELECT * FROM pendingPasswordResets")
    results = cursor.fetchall()
    return [i[1] for i in results]


##==================================================================================================================##
##==============================================  Pending Accounts  ================================================##
##==================================================================================================================##


def confirmPendingAccount(key):
    """ Removes the record with the provided 'key' (string) in it from the 'pendingAccounts' table in the DB
        and adds a new entry with the existing info (user_email and user_password) to the 'users' table """
    # Get info
    cursor.execute("SELECT * FROM pendingAccounts WHERE confirmation_key=?", (key,))
    results = cursor.fetchall()
    # Delete from 'pendingAccounts' table in the DB
    cursor.execute("DELETE FROM pendingAccounts WHERE confirmation_key=?", (key,))
    # Add to the 'users' table in the DB
    addUser(results[0][0], results[0][2])
    connection.commit()


def alreadyInPendingAccounts(userEmail):
    """ Checks in the 'pendingAccounts' table in the DB to see if that user has already sent a confirmation email
    Input:
    userEmail (str) = the email of the user being looked for in the database
    Output:
    True (bool) = the data was found
    False (bool) = the data wasn't found """
    cursor.execute("SELECT * FROM pendingAccounts WHERE user_email=?", (userEmail,))
    results = cursor.fetchall()
    if results:
        return True
    else:
        return False


def addToPendingAccounts(userEmail, confirmationKey, userPassword):
    """ Adds the given data (all strings) to the 'pendingAccounts' table in the DB """
    cursor.execute("INSERT INTO pendingAccounts (user_email, confirmation_key, user_password) VALUES (?, ?, ?)", (userEmail, confirmationKey, userPassword))
    connection.commit()


def keysInPendingAccounts():
    """ Returns all the keys that are in use by the 'pendingAccounts' table in the DB as a list of strings """
    cursor.execute("SELECT * FROM pendingAccounts")
    results = cursor.fetchall()
    return [i[1] for i in results]


##==================================================================================================================##
##===========================================  Pending Student Requests  ===========================================##
##==================================================================================================================##


def confirmPendingStudentRequest(key):
    """ Removes the record with the provided 'key' (string) in it from the 'pendingStudentRequests' table in the DB
        and adds a new entry with the existing info (student_email and user_email) to the 'students' table """
    # Get info
    cursor.execute("SELECT * FROM pendingStudentRequests WHERE confirmation_key=?", (key,))
    results = cursor.fetchall()
    # Delete from 'pendingStudentRequests' table in the DB
    cursor.execute("DELETE FROM pendingStudentRequests WHERE confirmation_key=?", (key,))
    # Add to the 'students' table in the DB
    addStudent(results[0][0], results[0][2])
    connection.commit()


def alreadyInPendingStudentRequests(studentEmail, userEmail):
    """ Checks in the 'pendingStudentRequests' table in the DB to see if that user has already sent a request to that student
    Input:
    studentEmail (str) = the email of the student being looked for in the database
    userEmail (str) = the email of the user being looked for in the database
    Output:
    True (bool) = the data was found
    False (bool) = the data wasn't found """
    cursor.execute("SELECT * FROM pendingStudentRequests WHERE student_email=? AND user_email=?", (studentEmail, userEmail))
    results = cursor.fetchall()
    if results:
        return True
    else:
        return False


def addToPendingStudentRequests(studentEmail, confirmationKey, userEmail):
    """ Adds the given data (all strings) to the 'pendingStudentRequests' table in the DB """
    cursor.execute("INSERT INTO pendingStudentRequests (student_email, confirmation_key, user_email) VALUES (?, ?, ?)", (studentEmail, confirmationKey, userEmail))
    connection.commit()


def keysInPendingStudentRequests():
    """ Returns all the keys that are in use by the 'pendingStudentRequests' table in the DB as a list of strings """
    cursor.execute("SELECT * FROM pendingStudentRequests")
    results = cursor.fetchall()
    return [i[1] for i in results]


##==================================================================================================================##
##====================================================  Users  =====================================================##
##==================================================================================================================##


def userEmailInUse(userEmail):
    """ Checks in the 'users' table in the DB to see if that user email (string) is already in use,
    returns True (bool) if it is otherwise it returns False (bool) """
    cursor.execute("SELECT * FROM users WHERE user_email=?", (userEmail,))
    results = cursor.fetchall()
    if results:
        return True
    else:
        return False


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


def addUser(userEmail, userPassword):
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


def deleteUser(userEmail):
    """ Deletes the user corresponding to the provided email (string) from the database.
        Returns True (bool) if it was successful or False (bool) if the user doesn't exist. """
    if userEmailInUse(userEmail):
        cursor.execute("DELETE FROM users WHERE user_email=?", (userEmail,))
        cursor.execute("DELETE FROM students WHERE user_email=?", (userEmail,))
        cursor.execute("DELETE FROM pendingStudentRequests WHERE user_email=?", (userEmail,))
        cursor.execute("DELETE FROM pendingAccounts WHERE user_email=?", (userEmail,))
        cursor.execute("DELETE FROM pendingPasswordResets WHERE user_email=?", (userEmail,))
        cursor.execute("DELETE FROM pendingDeletedAccounts WHERE user_email=?", (userEmail,))
        connection.commit()
        return True
    else:
        return False


##==================================================================================================================##
##===================================================  Students  ===================================================##
##==================================================================================================================##


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

def deleteStudent(studentEmail, userEmail):
    """ Deletes the student-user affiliation corresponding to the provided emails (strings) in the database.
        Returns True (bool) if it was successful or False (bool) if it wasn't found in the DB. """
    if studentEmail in getStudents(userEmail):
        cursor.execute("DELETE FROM students WHERE student_email=? AND user_email=?", (studentEmail, userEmail))
        connection.commit()
        return True
    else:
        return False
