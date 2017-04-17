from functools import wraps
from flask import *
import sqlAPI
import emailPackage
import randomKey

app = Flask(__name__)
app.secret_key="v\xf1\xb5\tr\xe2\xb3\x14!g"

def loginState():
    if 'username' in session:
        return True
    else:
        return False


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:    
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function


def logged_out_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:    
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
        userInfo = sqlAPI.getUserData(request.form["email"], request.form["password"])
        if userInfo:
            session["username"] = userInfo["email"]
            session["uid"] = userInfo["uid"]
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
        email = request.form["email"]
        password = request.form["password"]
        repeatPassword = request.form["repeatPassword"]
        # Verify the data that was provided by the user and try to add it to the database
        if password == repeatPassword:
            if sqlAPI.insertData(email, password):
                # Login the user
                userInfo = sqlAPI.getUserData(request.form["email"], request.form["password"])
                if userInfo:
                    session["username"] = userInfo["email"]
                    session["uid"] = userInfo["uid"]
                    flash("You successfully signed up!")
                    return redirect(url_for("home"))
                else:
                    print("Something went wrong; app.py; signup()")
                    return redirect(url_for("login"))
            else: # If the username was already in use
                error = "Oops! The username '{}' is already in use.".format(email)
        else:
            error = "Oops! The passwords you entered did not match"
    return render_template("signup.html", error=error, loginState=loginState())


@app.route("/")
def home():
    return render_template("index.html", messages=get_flashed_messages(), loginState=loginState())
    

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    if request.method == "POST":
        session.pop("username")
        return redirect(url_for("home"))
    return render_template("logout.html", loginState=loginState())


#NOTE I ALSO NEED TO ADD A CONDITION THAT CHECKS IF THE STUDENT IS IN THE DB ON THE PI
@app.route("/mystudents", methods=["GET", "POST"])
@login_required
def mystudents():
    error = None
    currentStudents = sqlAPI.getStudents(session["uid"])
    if request.method == "POST":
        studentEmail = request.form["studentEmail"]
        if studentEmail not in currentStudents:
            if not sqlAPI.alreadyInPendingRequests(studentEmail, session["username"]):
                # Send email
                randKey = randomKey.createRandomKey(sqlAPI.keysInUse())
                emailSent = emailPackage.sendEmail(studentEmail, session['username'], randKey)
                if emailSent:
                    sqlAPI.addToPendingRequests(studentEmail, randKey, session['uid'])
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


@app.route("/confirm/<key>", methods=["GET"])
def confirm(key):
    # Check if that key has already been confirmed
    if key in sqlAPI.keysInUse():
        sqlAPI.confirmKey(key)
        flash("Successfully confirmed.")
    else:
        flash("Oops! This <smthn> has already been confirmed.")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()
