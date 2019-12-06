from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
import sqlite3
from auth import auth
from services import monitoring

webclient = Flask(__name__, static_url_path='', static_folder='web_front/static', template_folder='web_front/templates')
webclient.secret_key = "secretkey"

@webclient.route("/")
def reroute():
    return redirect("/login")

@webclient.route("/login", methods=["GET", "POST"])
def login():
    message = None

    # If a user is already logged in, log them out
    if(session.get("logged_in") == True):
        session.clear()

    if request.method == "POST":
        # Use custom auth module to login
        session["userid"], message = auth.login(session, request)

        if session.get("logged_in"):
            # log, then redirect
            monitoring.log("authentication", (session["userid"], request.form["username"]))
            return redirect("/home")

    # If not already redirected to /home, then redirect back to login and print the error message
    return render_template("login.html", message=message)

@webclient.route("/createuser", methods=["GET", "POST"])
def createUser():
    message = None
    if request.method == "POST":
        # Use custom auth module to create account
        message = auth.createUser(session, request)

    return render_template("createuser.html", message=message)

@webclient.route("/home", methods=["GET", "POST"])
def home():
    # If not logged in, redirect back to login page
    #if not session.get('logged_in'):
    #    return redirect("/login")
    #else:
        conn = sqlite3.connect('flowers2019.db')
        cc = conn.execute('SELECT comname FROM Flowers')
        items = cc.fetchall()
        #for row in cc:
        #    print("comname = ", row[0], "\n")

        return render_template("home.html", items=items)

@webclient.route("/flowerinfo", methods=["GET", "POST"])
def display():
    return render_template("flowerinfo.html")

@webclient.route("/insert", methods=["GET", "POST"])
def insert():
    return render_template("insert.html")

@webclient.route("/update", methods=["GET", "POST"])
def update():
    return render_template("update.html")
if __name__ == "__main__":
    webclient.run()
