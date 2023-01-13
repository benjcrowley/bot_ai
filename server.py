from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, abort
from datetime import datetime
import crud
from werkzeug.security import generate_password_hash, check_password_hash
from model import connect_to_db, db, User, Script, Reviews
import os
app = Flask(__name__)
app.secret_key = "secret key"




@app.route("/")
def home():
    return render_template("home.html")

# a route for the catalog page of all the python scripts available for download from the scripts db
@app.route("/catalog")
def catalog():
    # Function to retrieve the list of items from the database or other source
    items = crud.view_all_scripts()
    for script in items:
        script.average = crud.get_script_rating(script.id)
    return render_template("catalog.html", items=items)


# a route for the download page of the python script
@app.route("/download/<script_id>")
def download(script_id):
    script = crud.get_script_by_id(script_id)
    return send_file("//Users/bennettcrowley/development/bot_ai/scripts_for_dwnload/" + script.file_name, as_attachment=True)

# a route for the about page
@app.route("/about")
def about():
    return render_template("about.html")

# a route for the contact page
@app.route("/contact")
def contact():
    return render_template("contact.html")
# a route for a log in page
@app.route("/login", methods=["GET", "POST"])
def login():
    '''Log in user'''
    if request.method == "POST":
        email_username = request.form.get("username")
        password = request.form.get("password")
        # print(request.form)
        user = crud.get_user(email_username)
        print(user)
        if user:
            print('user found')
            if user.password == password:
                print('password correct')
                session["user_id"] = user.id
                session["username"] = user.username
                print("Logged in successfully")
                return redirect(url_for("home"))
            else:
                print('incorrect password')

        return render_template("login.html")

    else:
        return render_template("login.html")

# a route for the signup page that will allow users to create an account and hash the password
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        print(request.form)

        user = crud.get_user(email)

        if user:
            return "User already exists"
        else:
            user = crud.create_user(username, email, password)
            return redirect(url_for("login"))

    return render_template("signup.html")
# a route for the logout page
@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.clear()
    return render_template("logout.html")

# a route for the terms and condtions page
@app.route("/terms")
def terms():
    return render_template("terms.html")

if __name__ == "__main__":
    connect_to_db(app)
    secret_key = os.environ.get("SECRET_KEY")
    app.run(debug=True, port=5001)