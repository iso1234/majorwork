from functools import wraps
from flask import *
import sqlAPI

app = Flask(__name__)
app.secret_key="v\xf1\xb5\tr\xe2\xb3\x14!g"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:    
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function
    

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        # Check if the provided credentials are valid
        if sqlAPI.userInDB(request.form["email"], request.form["password"]):
            session['username'] = request.form["email"]
            flash("You were successfully logged in!")
            return redirect(url_for("home"))
        else:
            error = "Oops! Wrong username/password."
    return render_template("login.html", error=error)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        repeatPassword = request.form["repeatPassword"]
        # Verify the data that was provided by the user and try to add it to the database
        if password == repeatPassword:
            if sqlAPI.insertData(email, password):
                flash("You successfully signed up!")
                return redirect(url_for("home"))
            else: # If the username was already in use
                error = "Oops! The username '{}' is already in use.".format(email)
        else:
            error = "Oops! The passwords you entered did not match"
    return render_template("signup.html", error=error)


@app.route("/")
def home():
    return render_template("index.html", messages=get_flashed_messages())
    

@app.route("/logout")
@login_required
def logout():
    return ""


if __name__ == "__main__":
    app.run()
