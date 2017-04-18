from functools import wraps
from flask import *
import sqlAPI
import emailPackage
import randomKey

app = Flask(__name__)
app.secret_key="v\xf1\xb5\tr\xe2\xb3\x14!g"

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
    return render_template("login.html", error=error, loginState=loginState())


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
                    emailSent = emailPackage.sendEmail(signupEmail, signupEmail, randKey, "a")
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
    return render_template("signup.html", error=error, loginState=loginState())


@app.route("/confirmAccount/<key>", methods=["GET"])
def confirmAccount(key):
    # Check if that key has already been confirmed
    if key in sqlAPI.keysInPendingAccounts():
        sqlAPI.confirmPendingAccount(key)
        flash("Successfully confirmed.")
    else:
        flash("Oops! This request has already been confirmed.")
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("index.html", messages=get_flashed_messages(), loginState=loginState())
    

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    if request.method == "POST":
        session.pop("userEmail")
        return redirect(url_for("home"))
    return render_template("logout.html", loginState=loginState())


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
                emailSent = emailPackage.sendEmail(studentEmail, session['userEmail'], randKey, "s")
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
    return render_template("mystudents.html", loginState=loginState(), currentStudents=currentStudents, error=error)


@app.route("/confirmStudentRequest/<key>", methods=["GET"])
def confirmStudentRequest(key):
    # Check if that key has already been confirmed
    if key in sqlAPI.keysInPendingStudentRequests():
        sqlAPI.confirmPendingStudentRequest(key)
        flash("Successfully confirmed.")
    else:
        flash("Oops! This request has already been confirmed.")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()
