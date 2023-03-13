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
get_reports() method used to display the reports template to the user upon
visiting the site.
"""


@app.route("/")
@app.route("/get_reports")
def get_reports():
    reports = mongo.db.reports.find()
    return render_template("reports.html", reports=reports)


"""
register() method used to display the register template to the site and to
gather the user input data from the register form and post it to the database.
"""


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # checking whether the user name from form already exists
        # in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("This username already exists, please try again!")
            return redirect(url_for('register'))

        register = {
            "username": request.form.get("username").lower(),
            "fname": request.form.get("fname").lower(),
            "lname": request.form.get("lname").lower(),
            "county": request.form.get("county").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # putting the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Your registration has been successful!")

    return render_template("register.html")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
