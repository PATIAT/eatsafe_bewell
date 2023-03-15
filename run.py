import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)

"""
The get_reports() function is used to display the reports summary template
to the user upon visiting the site.
"""


@app.route("/")
@app.route("/get_reports")
def get_reports():
    reports = list(mongo.db.reports.find())
    return render_template("reports.html", reports=reports)


"""
The register() function is used to display the register template to the site
and to gather the user input data from the registration form and post it to
the database.
"""


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # checking whether the user name from form already exists
        # in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        if existing_user:
            flash("This username already exists, please try again!")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "fname": request.form.get("fname").lower(),
            "lname": request.form.get("lname").lower(),
            "county": request.form.get("county").lower(),
            "password": generate_password_hash(request.form.get("password")),
        }
        mongo.db.users.insert_one(register)

        # putting the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Your registration has been successful!")
        return redirect(url_for("dashboard", username=session["user"]))

    return render_template("register.html")


"""
The login() function renders the html template using GET method and POST
checks to see if the database has the username. If so, the password given
by the user is checked to ensure it matches with the werkzeug hashed
password. If the password doesn't match or if the username doesn't match
or exist, the user is presented with flash messages to inform them and are
redirected to the same login page.
"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # checking if the username from the user matches any
        # database records
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        if existing_user:
            # checking if the hashed password from the user matches
            # any database records
            if check_password_hash(
                existing_user["password"], request.form.get("password")
            ):

                session["user"] = request.form.get("username").lower()
                flash(
                    "Welcome to Eat safe, be well, {}".format(
                        request.form.get("username")
                    )
                )
                return redirect(url_for("dashboard", username=session["user"]))

            else:
                # message to user to let them know the username and/or
                # password provided is incorrect
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # message to user to let them know the username and/or
            # password provided is incorrect
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


"""
The dashboard() function gets the session user's username from
the database and redirects the user to their own dashboard.

"""


@app.route("/dashboard/<username>", methods=["GET", "POST"])
def dashboard(username):
    # retrieving the session user username from the database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("dashboard.html", username=username)

    return redirect(url_for("login"))


"""
The logout() function removes the session user's cookie and provides
the user with a flash message before redirecting them to the login
screen again.

"""


@app.route("/logout")
def logout():
    # removing the user from session cookies and logging user out
    flash("You have successfully logged out")
    session.pop("user")
    return redirect(url_for("login"))


"""
The add_report() function renders the add report template and connects
the database categories to the form select list.

"""


@app.route("/add_report")
def add_report():
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_report.html", categories=categories)


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
