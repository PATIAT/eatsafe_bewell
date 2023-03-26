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
The search() function is used index the database using report_name and
report_description to match results to the users input.
"""


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    reports = list(mongo.db.reports.find({"$text": {"$search": query}}))
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
    user_reports = list(
        mongo.db.reports.find({"reported_by": session["user"]}))

    if session["user"]:
        return render_template(
            "dashboard.html", username=username, user_reports=user_reports)

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
the database categories to the form select list. If the requested method
from user input is POST, it executes function and adds all fields to
the database. If GET, the blank form is displayed.

"""


@app.route("/add_report", methods=["GET", "POST"])
def add_report():
    if request.method == "POST":
        is_serious = "on" if request.form.get("is_serious") else "off"
        report_fbo = "on" if request.form.get("report_fbo") else "off"
        report = {
            "report_name": request.form.get("report_name"),
            "report_product": request.form.get("report_product"),
            "report_product": request.form.get("report_product"),
            "report_brand": request.form.get("report_brand"),
            "report_bbd": request.form.get("report_bbd"),
            "category_name": request.form.get("category_name"),
            "report_symptoms": request.form.get("report_symptoms"),
            "is_serious": is_serious,
            "report_fbo": report_fbo,
            "report_date": request.form.get("report_date"),
            "reported_by": session["user"]
        }
        mongo.db.reports.insert_one(report)
        flash("Report Successfully Submitted")
        return redirect(url_for("get_reports"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_report.html", categories=categories)


"""
The edit_report() function renders the edit report template to users
but also find the report id from the database and allows the user to
edit it while displayig the existing data to the user
"""


@app.route("/edit_report/<report_id>", methods=["GET", "POST"])
def edit_report(report_id):
    if request.method == "POST":
        is_serious = "on" if request.form.get("is_serious") else "off"
        report_fbo = "on" if request.form.get("report_fbo") else "off"
        submit = {
            "report_name": request.form.get("report_name"),
            "report_product": request.form.get("report_product"),
            "report_product": request.form.get("report_product"),
            "report_brand": request.form.get("report_brand"),
            "report_bbd": request.form.get("report_bbd"),
            "category_name": request.form.get("category_name"),
            "report_symptoms": request.form.get("report_symptoms"),
            "is_serious": is_serious,
            "report_fbo": report_fbo,
            "report_date": request.form.get("report_date"),
            "reported_by": session["user"]
        }
        mongo.db.reports.update_one(
            {"_id": ObjectId(report_id)}, {"$set": submit})
        flash("Report Successfully Edited")

    report = mongo.db.reports.find_one({"_id": ObjectId(report_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "edit_report.html", report=report, categories=categories)


"""
The delete_report() function takes report id as a parameter by using the
object and report id. This is removed by using the delete_one method
and the user is provided with a flash message and then redirected to the
get reports page.
"""


@app.route("/delete_report/<report_id>")
def delete_report(report_id):
    report = mongo.db.reports.find_one({"_id": ObjectId(report_id)})
    if not report:
        flash("Report not found")
        return redirect(url_for("get_reports"))
    return render_template("confirm_delete.html", report_id=report_id)


"""
The delete_report_confirmed() method confirms whether the method is POST,
if so, the report is deleted from the database and the user is redirected
back to the reports page. If the method is not POST (i.e. it's GET or
something else), we flash an error message and redirect the user back to
the reports page.
"""


@app.route("/delete_report_confirmed/<report_id>", methods=["GET", "POST"])
def delete_report_confirmed(report_id):
    if request.method == "POST":
        mongo.db.reports.delete_one({"_id": ObjectId(report_id)})
        flash("Report Successfully Deleted")
        return redirect(url_for("get_reports"))
    else:
        flash("Invalid request method")
        return redirect(url_for("get_reports"))


"""
The get_categories() method find the categories from the database and renders
them to the template for the user to view.
"""


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


"""
The add_category() function renders the add category template and connects
the database categories to the form select list. If the requested method
from user input is POST, it executes function and adds the new category to
the database. If GET, the blank form is displayed.

"""


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.insert_one(category)
        flash("New Category Added")
        return redirect(url_for("get_categories"))

    return render_template("add_category.html")


"""
The edit_category() function renders the edit category template to users
but also finds the category id from the database and allows the user to
edit it while displayig the existing data to the user.
"""


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.update_one(
            {"_id": ObjectId(category_id)}, {"$set": submit})
        flash("Category Updated Successfully")
        return redirect(url_for("get_categories"))

    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


"""
The delete_category() function takes category id as a parameter by using the
object and category id. This is removed by using the remove method
and the user is provided with a flash message and then redirected to the
get categories page.
"""


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    if not category:
        flash("Category not found")
        return redirect(url_for("get_categories"))
    return render_template(
        "confirm_delete_category.html", category_id=category_id)


"""
The delete_category_confirmed() method confirms whether the method is POST,
if so, the cetegory is deleted from the database and the user is redirected
back to the categories page. If the method is not POST (i.e. it's GET or
something else), we flash an error message and redirect the user back to
the categories page.
"""


@app.route("/delete_category_confirmed/<category_id>", methods=["GET", "POST"])
def delete_category_confirmed(category_id):
    if request.method == "POST":
        mongo.db.categories.delete_one({"_id": ObjectId(category_id)})
        flash("Category Successfully Deleted")
        return redirect(url_for("get_categories"))
    else:
        flash("Invalid request method")
        return redirect(url_for("get_categories"))


"""
The page_not_found() method returns a custom 404 error page. It
registers this view function as the error handler for 404 errors
using the @app.errorhandler(404) decorator. Inside the page_not_found
function, the render_template function renders the HTML template.
It also returns a 404 status code to the browser by passing the second
argument 404 to the render_template function.
This function was sourced from Flask documentation.
"""


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


"""
The about() function simply renders the about page.
"""


@app.route("/about")
def about():
    return render_template("about.html")


"""
The why_report() function simply renders the why report? page.
"""


@app.route("/why_report")
def why_report():
    return render_template("why_report.html")


# Run the app
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
