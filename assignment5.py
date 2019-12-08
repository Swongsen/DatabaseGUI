from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
import sqlite3
from auth import auth
from services import monitoring

webclient = Flask(__name__, static_url_path='', static_folder='web_front/static', template_folder='web_front/templates')
webclient.secret_key = "secretkey"

# initializing global variables
flower = "a"
items = ""
option = ""

# Base route. Reroutes to login
@webclient.route("/")
def reroute():
    return redirect("/login")

# Login page
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

# Create an account page
@webclient.route("/createuser", methods=["GET", "POST"])
def createUser():
    message = None
    if request.method == "POST":
        # Use custom auth module to create account
        message = auth.createUser(session, request)

    return render_template("createuser.html", message=message)

# Home page
@webclient.route("/home", methods=["GET", "POST"])
def home():
    global flower
    global value
    # If not logged in, redirect back to login page
    if not session.get('logged_in'):
        return redirect("/login")
    else:
     if request.method == "GET":
        # Opens database and selects comname to return to items
        conn = sqlite3.connect('flowers2019.db')
        cc = conn.execute('SELECT comname FROM Flowers')
        items = cc.fetchall()
        conn.close()
        #for row in cc:
        #    print("comname = ", row[0], "\n")

        return render_template("home.html", items=items)

     elif request.method == "POST":
        # Title captures the flowername
        flower = request.form["flowername"]
        # Value is the option chose on the home screen
        value = request.form["option"]
        #print("flower:", flower)
        print("option:", value)

        # Reroutes to selected option
        if value == "Insert Sighting":
            return redirect("/insert")
        elif value == "Sightings":
            return redirect("/flowersightings")
        elif value == "Update Flower":
            return redirect("/update")
        elif value == "Delete Sighting":
            return redirect("/deletesighting")

@webclient.route("/deletesighting", methods=["GET", "POST"])
def delete():
    global flower
    message = None
    # Connects to the database
    conn = sqlite3.connect('flowers2019.db')

    # When loading page
    if request.method == "GET":

        return render_template("deletesighting.html",flower=flower)

    # When sending info from page
    elif request.method == "POST":
        message = "Sighting deleted"
        person = request.form["person"]
        location = request.form["location"]
        sighting = request.form["sighted"]

        cc = conn.execute('DELETE FROM SIGHTINGS WHERE NAME = \"'+flower+'\" AND PERSON = \"'+person+'\" AND LOCATION = \"'+location+'\" AND SIGHTED = \"'+sighting+'\"')
        conn.commit()

        return render_template("deletesighting.html", message=message)

@webclient.route("/flowersightings", methods=["GET", "POST"])
def display():
    global flower
    global items

    if request.method == "GET":
        items = ""
        conn = sqlite3.connect('flowers2019.db')
        cc = conn.execute('SELECT PERSON, LOCATION, SIGHTED FROM SIGHTINGS WHERE NAME IN (SELECT COMNAME FROM FLOWERS WHERE COMNAME = \"'+flower+'\") ORDER BY SIGHTINGS.SIGHTED DESC LIMIT 10' )
        items = cc.fetchall()
        print(flower)
        title = flower

        return render_template("flowersightings.html", items=items, flower=flower)

@webclient.route("/insert", methods=["GET", "POST"])
def insert():
    global flower
    message = None
    conn = sqlite3.connect('flowers2019.db')

    if request.method == "GET":
        return render_template("insert.html", flower = flower)

    elif request.method == "POST":
        message = "Sighting inserted"
        person = request.form["person"]
        location = request.form["location"]
        sighting = request.form["sighted"]

        cc = conn.execute('INSERT INTO SIGHTINGS (NAME, PERSON, LOCATION, SIGHTED) VALUES (\"'+flower+'\",\"'+person+'\",\"'+location+'\",\"'+sighting+'\")')
        conn.commit()

        return render_template("insert.html", message=message)

@webclient.route("/update", methods=["GET", "POST"])
def update():
    global flower
    message = None
    conn = sqlite3.connect('flowers2019.db')

    if request.method == "GET":
        # Pass the flower name to the template
        return render_template("update.html", flower=flower)

    elif request.method == "POST":

        message="Updated Successfully"
        originalperson = request.form["person"]
        originallocation = request.form["location"]
        originalsighting = request.form["sighted"]

        updateperson = request.form["updatedperson"]
        updatelocation = request.form["updatedlocation"]
        updatesighting = request.form["updatedsighted"]

        cc = conn.execute('UPDATE SIGHTINGS SET Person =\"'+updateperson+'\", Location =\"'+updatelocation+'\", Sighted =\"'+updatesighting+'\" WHERE Person =\"'+originalperson+'\" AND Location =\"'+originallocation+'\" AND Sighted =\"'+originalsighting+'\" AND name =\"'+flower+'\"')
        conn.commit()

        print("flower:", flower)
        print(originalperson, originallocation, originalsighting)
        print(updateperson, updatelocation, updatesighting)
        return render_template("update.html", message=message)



if __name__ == "__main__":
    webclient.run()
