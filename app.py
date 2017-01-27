from flask import *
app = Flask(__name__)
app.secret_key="Bananna"

@app.route("/login", methods=["GET", "POST"])
def handleLogin():
    error = None
    if request.method == "POST":
        if request.form["email"] == "admin@admin.com" and request.form["password"] == "admin":
            flash("You were successfully logged in!")
            return redirect(url_for("home"))
        else:
            error = "Oops! Wrong username/password."
            
    return render_template("login.html", error=error)

@app.route("/")
def home():
    return render_template("index.html", messages=get_flashed_messages())

if __name__ == "__main__":
    app.run()
