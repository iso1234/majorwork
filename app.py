from functools import wraps
from flask import Flask, redirect, url_for, request, session, flash, get_flashed_messages
import sqlAPI
import emailPackage
import randomKey
from templateEngine import renderTemplate

app = Flask(__name__)
app.secret_key="v\xf1\xb5\tr\xe2\xb3\x14!g"

IP = "127.0.0.1"
PORT = "5000"
ADDRESS = IP + ":" + PORT

def loginState():
    """ Returns True if the user is logged in, otherwise it returns false """
    if 'userEmail' in session:
        return True
    else:
        return False


def login_required(f):
    """ A decorator used to restrict functions (pages in the website) to users that are logged in """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If the user is looged in
        if 'userEmail' in session:    
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function


def logged_out_required(f):
    """ A decorator used to restrict functions (pages in the website) to users that are logged out """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If the user isn't logged in
        if 'userEmail' not in session:    
            return f(*args, **kwargs)
        else:
            return redirect(url_for('logout'))
    return decorated_function
    

@app.route("/login", methods=["GET", "POST"])
@logged_out_required
def login():
    error = None
    if request.method == "POST":
        # Check if the provided credentials are valid
        validCredentials = sqlAPI.userInDB(request.form["userEmail"], request.form["userPassword"])
        if validCredentials:
            session["userEmail"] = request.form["userEmail"]
            flash("You were successfully logged in!")
            return redirect(url_for("home"))
        else:
            error = "Oops! Wrong username/password."
    return renderTemplate("login.html", {"error": error, "loginState": loginState()})


@app.route("/signup", methods=["GET", "POST"])
@logged_out_required
def signup():
    error = None
    if request.method == "POST":
        signupEmail = request.form["signupEmail"]
        signupPassword = request.form["signupPassword"]
        signupRepeatPassword = request.form["signupRepeatPassword"]
        # Verify the data that was provided by the user and send a confirmation email
        if signupPassword == signupRepeatPassword:
            if not sqlAPI.userEmailInUse(signupEmail):
                if not sqlAPI.alreadyInPendingAccounts(signupEmail):
                    # Send email
                    randKey = randomKey.createRandomKey(sqlAPI.keysInPendingAccounts())
                    emailSent = emailPackage.sendEmail(signupEmail, signupEmail, randKey, "a", ADDRESS)
                    if emailSent:
                        sqlAPI.addToPendingAccounts(signupEmail, randKey, signupPassword)
                        flash("Email successfully sent! Please check your email to confirm your account.")
                        return redirect(url_for("home"))
                    else:
                        # Email didn't work
                        error = "Oops! The confimation email could not be sent. Please check the email address and try again later."
                else:
                    # Already pending request
                    error = "Oops! A confirmation email has been sent to '{}', please use it to confirm your account and login.".format(signupEmail)
            else: # If the username was already in use
                error = "Oops! The username '{}' is already in use.".format(signupEmail)
        else:
            error = "Oops! The passwords you entered did not match"
    return renderTemplate("signup.html", {"error": error, "loginState": loginState()})


@app.route("/confirmAccount/<key>")
def confirmAccount(key):
    # Check if that key has already been confirmed
    if key in sqlAPI.keysInPendingAccounts():
        sqlAPI.confirmPendingAccount(key)
        flash("Account successfully confirmed.")
    else:
        flash("Oops! This request has already been confirmed or the associated account has been deleted.")
    return redirect(url_for("home"))


@app.route("/")
def home():
    return renderTemplate("index.html", {"messages": get_flashed_messages(), "loginState": loginState()})
    

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    if request.method == "POST":
        session.pop("userEmail")
        return redirect(url_for("home"))
    return renderTemplate("logout.html", {"loginState": loginState()})


#NOTE I ALSO NEED TO ADD A CONDITION THAT CHECKS IF THE STUDENT IS IN THE DB ON THE PI
@app.route("/mystudents", methods=["GET", "POST"])
@login_required
def mystudents():
    error = None
    currentStudents = sqlAPI.getStudents(session["userEmail"])
    if request.method == "POST":
        studentEmail = request.form["studentEmail"]
        if studentEmail not in currentStudents:
            if not sqlAPI.alreadyInPendingStudentRequests(studentEmail, session["userEmail"]):
                # Send email
                randKey = randomKey.createRandomKey(sqlAPI.keysInPendingStudentRequests())
                emailSent = emailPackage.sendEmail(studentEmail, session['userEmail'], randKey, "s", ADDRESS)
                if emailSent:
                    sqlAPI.addToPendingStudentRequests(studentEmail, randKey, session['userEmail'])
                    flash("Email successfully sent! Please get the student that was registered to check their email.")
                    return redirect(url_for("home"))
                else:
                    # Email didn't work
                    error = "Oops! The confimation email could not be sent. Please check the email address and try again later."
            else:
                # Already pending request
                error = "Oops! You've already sent a request email to the student with the email address {}.".format(studentEmail)
        else:
            # Already registered
            error = "Oops! You've already registered the student with the email address {}.".format(studentEmail)
    return renderTemplate("mystudents.html", {"loginState": loginState(), "studentInfo": sqlAPI.getStudentInfo(session["userEmail"]), "error": error})


@app.route("/confirmStudentRequest/<key>")
def confirmStudentRequest(key):
    # Check if that key has already been confirmed
    if key in sqlAPI.keysInPendingStudentRequests():
        sqlAPI.confirmPendingStudentRequest(key)
        flash("Successfully confirmed.")
    else:
        flash("Oops! This request has already been confirmed or the associated user has deleted their account.")
    return redirect(url_for("home"))
    
    
@app.route("/sendResetPasswordEmail", methods=["POST"])
def sendResetPasswordEmail():
    if request.method == "POST":
        userEmail = request.form["userEmail"]
        # If the email is actually attached to an account
        if sqlAPI.userEmailInUse(userEmail):
            # If a reset email hasn't already been sent
            if not sqlAPI.alreadyInPendingPasswordResets(userEmail):
                # Send email
                randKey = randomKey.createRandomKey(sqlAPI.keysInPendingPasswordResets())
                emailSent = emailPackage.sendEmail(userEmail, userEmail, randKey, "r", ADDRESS)
                if emailSent:
                    sqlAPI.addToPendingPasswordResets(userEmail, randKey)
                    flash("Email successfully sent! Please check your email address.")
                    return redirect(url_for("home"))
                else:
                    # Email didn't work
                    error = "Oops! The confimation email could not be sent. Please check the email address and try again later."
            else:
                flash("Oops! A reset password email has already been sent to '{}', please use it to reset your password.".format(userEmail))
        else:
            # If the email is awaiting confirmation
            if sqlAPI.alreadyInPendingAccounts(userEmail):
                flash("Oops! A confirmation email has been sent to '{}', please use it to confirm your account and login.".format(userEmail))
            else:
                flash("Oops! That email isn't associated with an account, please enter the email associated with your account or register an account.")
    return redirect(url_for("home"))
    

@app.route("/resetPassword", methods=["POST"])    
@app.route("/resetPassword/<key>", methods=["GET"])
def resetPassword(key=""):
    if request.method == "GET":
        if key in sqlAPI.keysInPendingPasswordResets():
            return renderTemplate("resetpassword.html", {"key": key, "messages": get_flashed_messages()})
        else:
            flash("Oops! This password has already been reset or the associated account has been deleted.")
            return redirect(url_for("home"))
    elif request.method == "POST":
        if request.form["resetPassword"] == request.form["resetRepeatPassword"]:
            sqlAPI.resetPassword(request.form["resetKey"], request.form["resetPassword"])
            flash("Password successfully reset.")
            return redirect(url_for("home"))
        else:
            flash("Oops! The passwords you entered don't match. Please enter two matching passwords.")
            return redirect(url_for("resetPassword") + "/" + request.form["resetKey"])
            
@app.route("/deleteAccount", methods=["GET", "POST"])
@login_required
def deleteAccunt():
    error = None
    if request.method == "POST":
        if request.form["userEmail"] == session["userEmail"]:
            if sqlAPI.userInDB(request.form["userEmail"], request.form["userPassword"]):
                userEmail = request.form["userEmail"]
                if not sqlAPI.alreadyInPendingDeletedAccounts(userEmail):
                    # Send email
                    randKey = randomKey.createRandomKey(sqlAPI.keysInPendingDeletedAccounts())
                    emailSent = emailPackage.sendEmail(userEmail, userEmail, randKey, "d", ADDRESS)
                    if emailSent:
                        sqlAPI.addToPendingDeletedAccounts(userEmail, randKey)
                        flash("Email successfully sent! Visit your email to confirm the deletion of your account.")
                        return redirect(url_for("home"))
                    else:
                        # Email didn't work
                        error = "Oops! The confimation email could not be sent. Please check the email address and try again later."
                else:
                    # Already pending request
                    error = "Oops! You've already been sent a confirmation email to delete your account. You can use that email to delete you account."
            else:
                error = "Oops! Wrong username/password."
        else:
            error = "Oops! You must be logged into the account you want to delete."
    return renderTemplate("deleteAccount.html", {"loginState": loginState(), "error": error})


@app.route("/confirmDeleteAccount/<key>")
def confirmDeleteAccount(key):
    # Check if that key has already been confirmed
    if key in sqlAPI.keysInPendingDeletedAccounts():
        sqlAPI.confirmPendingDeletedAccount(key)
        if "userEmail" in session:
            session.pop("userEmail")
        flash("Account successfully deleted.")
        
    else:
        flash("Oops! This account has already been deleted.")
    return redirect(url_for("home"))
        

if __name__ == "__main__":
    app.run(host=IP)
