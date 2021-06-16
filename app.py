import sys
import os
from flask import Flask, flash, redirect, render_template, request, url_for, session
from flaskext.mysql import MySQL
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_session import Session
from database import Database
from makedb import MakeDB
from helpers import generate_weekID
import pymysql
from boto.s3.connection import S3Connection

# init flask app
app = Flask(__name__)
app.config['TESTING'] = False
# session secret key
app.secret_key = os.environ.get('SECRETKEYFLASK')
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Password Hashing
bcrypt = Bcrypt(app)

# init MySQL database
mysql = MySQL()
mysql.init_app(app)

#Make database if not EXISTS
MakeDB()

@app.route("/", methods=["GET", "POST"])
def index():
    #Call DB class to init database
    db=Database()

    if not session.get("user_id"):
        return redirect("/login")

    current_user = session["user_id"]

    if request.method == "POST":
        weekDates={}
        dayStatus={}
        days=["statusSaturday", "statusSunday", "statusMonday", "statusTuesday", "statusWednesday", "statusThursday", "statusFriday"]
        for i in range(0,7):
            weekDates[i]=request.form.get(f'td{i+1}')
            dayStatus[i]=request.form.get(days[i])
            if not weekDates[i]:
                flash("Please select date from datepicker!")
                return redirect(url_for("index"))
            if not dayStatus[i]:
                flash("Please select day status for all dates!")
                return redirect(url_for("index"))
        # DEBUG
        print(weekDates, file=sys.stderr)
        print(dayStatus, file=sys.stderr)

        weekID = generate_weekID(weekDates)
        try:
            db.timesheet_target(current_user, dayStatus, weekID)
        finally:
            db.close_cursor()

        flash(f'Timesheet successfully submitted for the week starting on {weekDates[0]}!')
        return redirect(url_for("index"))
    else:
        return render_template("timesheet.html", user = current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    """ User logs in here """
    error = None
    # Forget past user ids
    session.clear()
    #Call DB class to init database
    db=Database()

    # If user reached route via post method
    if request.method == "POST":
        email = request.form.get("email")
        email = email.strip()
        password = request.form.get("password")
        # print(username, password)
        if not email:
            # Return error message TODO
            error = "Please enter Email ID!"
            # return render_template('login.html', error=error)
            flash("Please enter Email ID!")
            return redirect(url_for("login"))
        elif not password:
            # Return error message TODO
            error = "Please enter password!"
            # return render_template('login.html', error=error)
            flash("Please enter password!")
            return redirect(url_for("/"))

        # Check login credentials from database
        try:
            rows = db.check_credentials_from_email(email)

            #DEBUG
            print(rows, file=sys.stderr)

            if len(rows)!=1 or not (bcrypt.check_password_hash(rows[0]["user_password"],password) or not (rows[0]["email_id"]==email)):
                error = "Invalid credentials"
                flash("Invalid credentials")
                # return redirect(url_for("login"))
                return render_template("login.html", error=error)
            # Remember which user has logged in
            session["user_id"] = rows[0]["EmployeeID"]
        finally:
            db.close_cursor()

        # redirect to main page
        flash('You were successfully logged in')
        return redirect("/")

    # User reached route via get method
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    # session.pop('username', None)
    session.clear()
    # redirect to main page
    return redirect("/")

@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None

    db=Database()

    if request.method == "POST":
        email = request.form.get("email")
        email=email.strip()
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if not request.form.get("first"):
            # Return error message TODO
            error = "First Name field missing"
            return error
        elif not request.form.get("last"):
            # Return error message TODO
            error = "Last Name field missing"
            return error
        elif not email:
            # Return error message TODO
            error = "Email field missing"
            return error
        elif not password:
            # Return error message TODO
            error = "Password field missing"
            return error
        elif not confirm:
            # Return error message TODO
            error = "Confirm password field missing"
            return error
        elif not request.form.get("dob"):
            # Return error message TODO
            error = "D.O.B. field missing"
            return error
        elif password != confirm:
            # Return error message # TODO
            error = "Passwords do not match"
            flash(error)
            return redirect(url_for("register"))

        try:
            # Check if user is in our database
            rows = db.check_exist(email)
            if len(rows)!=0:
                error = "User already exists"
                flash(error)
                return redirect(url_for("register"))
            else:
                # insert user details in database
                pw_hash = bcrypt.generate_password_hash(password)
                db.insert_user(email, pw_hash)
                emp_id = db.return_emp_id(email)
                db.insert_employee_details(emp_id, request.form.get("first").strip(), request.form.get("last").strip(), request.form.get("dob"))

        finally:
            db.close_cursor()

        flash("You have successfully registered!")
        return redirect(url_for("login"))
    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run()
