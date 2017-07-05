from functools import wraps
from flask import Flask, redirect, url_for, request, session, flash, get_flashed_messages
import sqlAPI
import emailPackage
import randomKey
from templateEngine import renderTemplate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key="v\xf1\xb5\tr\xe2\xb3\x14!g"

ADDRESS = "127.0.0.1"

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
    
    
@app.route("/")
def home():
    if loginState():
        # Logged in
        return renderTemplate("loggedIn.html", {"message": get_flashed_messages(), "loginState": loginState(), "studentInfo": sqlAPI.getStudentInfo(session["userEmail"])})
    else:
        # Logged out
        return renderTemplate("loggedOut.html", {"message": get_flashed_messages(), "loginState": loginState()})
    

@app.route("/login", methods=["POST"])
@logged_out_required
def login():
    # Check if the provided credentials are valid
    validCredentials = sqlAPI.userInDB(request.form["userEmail"], request.form["userPassword"])
    userEmail = request.form["userEmail"]
    if validCredentials:
        session["userEmail"] = userEmail
        # Delete any pending password requests from the db
        if sqlAPI.alreadyInPendingPasswordResets(userEmail):
            sqlAPI.deletePendingPasswordReset(userEmail)
        flash("success:You were successfully logged in!")
    else:
        flash("danger:Oops! Wrong username/password.")
    return redirect(url_for("home"))


@app.route("/signup", methods=["POST"])
@logged_out_required
def signup():
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
                    sqlAPI.addToPendingAccounts(signupEmail, randKey, generate_password_hash(signupPassword))
                    flash("success:Email successfully sent! Please use the email sent to '{}' to confirm your account.".format(signupEmail))
                else:
                    # Email didn't work
                    flash("danger:Oops! The confimation email could not be sent to '{}'. Please check the email address and try again later.".format(signupEmail))
            else:
                # Already pending request
                flash("danger:Oops! A confirmation email has already been sent to '{}', please use it to confirm your account.:Resend email".format(signupEmail))
        else: # If the username was already in use
            flash("danger:Oops! The username '{}' is already in use.".format(signupEmail))
    else:
        flash("danger:Oops! The passwords entered did not match.")
    return redirect(url_for("home"))


@app.route("/confirmAccount/<key>")
def confirmAccount(key):
    # Check if that key has already been confirmed
    if key in sqlAPI.keysInPendingAccounts():
        sqlAPI.confirmPendingAccount(key)
        flash("success:Account successfully confirmed.")
    else:
        flash("danger:Oops! This account has already been confirmed.")
    return redirect(url_for("home"))
    

@app.route("/logout")
@login_required
def logout():
    session.pop("userEmail")
    return redirect(url_for("home"))


@app.route("/mystudents", methods=["POST"])
@login_required
def mystudents():
    currentStudents = sqlAPI.getStudents(session["userEmail"])
    studentEmail = request.form["studentEmail"]
    if studentEmail not in currentStudents:
        if not sqlAPI.alreadyInPendingStudentRequests(studentEmail, session["userEmail"]):
            if sqlAPI.getStudentCardID(studentEmail):
                # Send email
                randKey = randomKey.createRandomKey(sqlAPI.keysInPendingStudentRequests())
                emailSent = emailPackage.sendEmail(studentEmail, session['userEmail'], randKey, "s", ADDRESS)
                if emailSent:
                    sqlAPI.addToPendingStudentRequests(studentEmail, randKey, session['userEmail'])
                    flash("success:Email successfully sent! Please use the email sent to '{}' to allow yourself access to this students information.".format(studentEmail))
                else:
                    # Email didn't work
                    flash("danger:Oops! The confimation email could not be sent to '{}'. Please check the email address and try again later.".format(studentEmail))
            else:
                 # Student isn't registered in the system
                flash("danger:Oops! '{}' isn't registered with our system.".format(studentEmail))
        else:
            # Already pending request
            flash("danger:Oops! You've already sent a request email to '{}'.:Resend email".format(studentEmail))
    else:
        # Already registered
        flash("danger:Oops! You've already registered the student '{}'.".format(studentEmail))
    return redirect(url_for("home"))


@app.route("/confirmStudentRequest/<key>")
def confirmStudentRequest(key):
    # Check if that key has already been confirmed
    if key in sqlAPI.keysInPendingStudentRequests():
        sqlAPI.confirmPendingStudentRequest(key)
        flash("success:Student successfully confirmed.")
    else:
        flash("danger:Oops! That request has already been confirmed or the associated user has deleted their account.")
    return redirect(url_for("home"))
    
    
@app.route("/sendResetPasswordEmail", methods=["POST"])
def sendResetPasswordEmail():
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
                flash("success:Email successfully sent! Please use the email sent to '{}' to reset your password.".format(userEmail))
            else:
                # Email didn't work
                flash("danger:Oops! The confimation email could not be sent to '{}'. Please check the email address and try again later.".format(userEmail))
        else:
            flash("danger:Oops! A reset password email has already been sent to '{}'. Please use it to reset your password.:Resend email".format(userEmail))
    else:
        # If the email is awaiting confirmation
        if sqlAPI.alreadyInPendingAccounts(userEmail):
            flash("danger:Oops! A confirmation email has already been sent to '{}', please use it to confirm your account and login.:Resend email".format(userEmail))
        else:
            flash("danger:Oops! The email '{}' isn't associated with an account, please enter the email associated with your account or register an account.".format(userEmail))
    return redirect(url_for("home"))
    

@app.route("/resetPassword", methods=["POST"])    
@app.route("/resetPassword/<key>", methods=["GET"])
def resetPassword(key=""):
    if request.method == "GET":
        if key in sqlAPI.keysInPendingPasswordResets():
            return renderTemplate("resetPassword.html", {"key": key, "message": get_flashed_messages(), "loginState": loginState()})
        else:
            flash("danger:Oops! This password has already been reset or the associated account has been deleted.")
            return redirect(url_for("home"))
    elif request.method == "POST":
        if request.form["resetPassword"] == request.form["resetRepeatPassword"]:
            sqlAPI.resetPassword(request.form["resetKey"], generate_password_hash(request.form["resetPassword"]))
            flash("success:Password successfully reset.")
            return redirect(url_for("home"))
        else:
            flash("danger:Oops! The passwords you entered don't match. Please enter two matching passwords.")
            return redirect(url_for("resetPassword") + "/" + request.form["resetKey"])


@app.route("/deleteAccount", methods=["POST"])
@login_required
def deleteAccount():
    if request.form["userEmail"] == session["userEmail"]:
        if sqlAPI.userInDB(request.form["userEmail"], request.form["userPassword"]):
            userEmail = request.form["userEmail"]
            if not sqlAPI.alreadyInPendingDeletedAccounts(userEmail):
                # Send email
                randKey = randomKey.createRandomKey(sqlAPI.keysInPendingDeletedAccounts())
                emailSent = emailPackage.sendEmail(userEmail, userEmail, randKey, "d", ADDRESS)
                if emailSent:
                    sqlAPI.addToPendingDeletedAccounts(userEmail, randKey)
                    flash("success:Email successfully sent. Visit the email '{}' to confirm the deletion of your account.".format(userEmail))
                else:
                    # Email didn't work
                    flash("danger:Oops! The confimation email could not be sent. to '{}' Please check the email address and try again later.".format(userEmail))
            else:
                # Already pending request
                flash("danger:Oops! You've already been sent a confirmation email to '{}'. Please use that email to delete you account.:Resend email".format(userEmail))
        else:
            flash("danger:Oops! Wrong username/password.")
    else:
        flash("danger:Oops! You must be logged into the account you want to delete.")
    return redirect(url_for("home"))


@app.route("/confirmDeleteAccount/<key>")
def confirmDeleteAccount(key):
    # Check if that key has already been confirmed
    if key in sqlAPI.keysInPendingDeletedAccounts():
        sqlAPI.confirmPendingDeletedAccount(key)
        if "userEmail" in session:
            session.pop("userEmail")
        flash("success:Account successfully deleted.")
        
    else:
        flash("danger:Oops! This account has already been deleted.")
    return redirect(url_for("home"))
        
@app.errorhandler(404)
def err(e):
    return renderTemplate("error.html", {})

if __name__ == "__main__":
    app.run(host=ADDRESS, port=80)
