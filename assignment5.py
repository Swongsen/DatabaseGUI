from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
import sqlite3
from auth import auth
from services import monitoring

webclient = Flask(__name__, static_url_path='', static_folder='web_front/static', template_folder='web_front/templates')
webclient.secret_key = "secretkey"
flower = "a"
items = ""

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
    global flower
    # If not logged in, redirect back to login page
    #if not session.get('logged_in'):
    #    return redirect("/login")
    #else:
    if request.method == "GET":
        conn = sqlite3.connect('flowers2019.db')
        cc = conn.execute('SELECT comname FROM Flowers')
        items = cc.fetchall()
        conn.close()
        #for row in cc:
        #    print("comname = ", row[0], "\n")

        return render_template("home.html", items=items)

    elif request.method == "POST":
        print("hello")
        title = request.form["flowername"]
        flower = title
        print("title: ", title)
        print("flower:", flower)
        return redirect("/flowerinfo")

@webclient.route("/flowerinfo", methods=["GET", "POST"])
def display():
    global flower
    global items

    if request.method == "GET":
        items = ""
        conn = sqlite3.connect('flowers2019.db')
        cc = conn.execute('SELECT PERSON, LOCATION, SIGHTED FROM SIGHTINGS, FLOWERS WHERE (FLOWERS.COMNAME = \"'+flower+'\") ORDER BY SIGHTINGS.SIGHTED DESC LIMIT 10' )
        items = cc.fetchall()
        print(flower)
        title = flower

        return render_template("flowerinfo.html", items=items)

@webclient.route("/insert", methods=["GET", "POST"])
def insert():
    global flower

    if request.method == "GET":
        return render_template("insert.html")

    elif request.method == "POST":
        return "HELLO"

@webclient.route("/update", methods=["GET", "POST"])
def update():
    global flower
    message = None
    conn = sqlite3.connect('flowers2019.db')

    if request.method == "GET":
        return render_template("update.html")

    elif request.method == "POST":
        message="Updated Successfully"
        originalperson = request.form["person"]
        originalflower = request.form["flowername"]
        originallocation = request.form["location"]
        originalsighting = request.form["sighted"]

        updateperson = request.form["updatedperson"]
        updateflower = request.form["updatedflowername"]
        updatelocation = request.form["updatedlocation"]
        updatesighting = request.form["updatedsighted"]

        cc = conn.execute('update sightings set name = \'' +updateflower +'\', person= \''+ updateperson+'\', location= \''+updatelocation+'\',sighted = \''+updatesighting
                           +'\' WHERE (name = \''+originalflower+'\' and person= \''+originalperson+'\' and location= \''+originallocation+'\' and sighted = \''+originalsighting+'\');')


        print(originalperson, originalflower, originallocation, originalsighting)
        print(updateperson, updateflower, updatelocation, updatesighting)
        return render_template("update.html", message=message)



if __name__ == "__main__":
    webclient.run()
