import pandas as pd
import os
import sys

user_data_path = os.path.dirname(os.path.abspath(__file__))+"\\users.csv"

# logs a user in if authentication succeeds
# returns a token and message if applicable
def login(session, request):
    userid = None
    message = None

    # Get the username and password from the request form
    user = request.form["username"]
    password = request.form["password"]

    user_data = pd.read_csv(user_data_path)

    # Reads the users csv to validate username password
    for index, row in user_data.iterrows():
        # If the username, password matches the username and password from the form
        if user == row["user"] and password == row["password"]:
            # Since there is match from users.csv, set the session to be logged in
            session["logged_in"] = True
            userid = row["id"]
            break
        else:
            message = "Invalid Credentials"

    return userid, message

# creates a user
def createUser(session, request):
    # Get the username and password from the request form
    user = request.form["username"]
    password = request.form["password"]

    if(len(password) < 8):
        message = "Password too short"
        return message

    user_data = pd.read_csv(user_data_path)
    user_data = user_data.set_index("id")

    account_exists = False
    # Reads the users csv to validate username does not already exist
    for index, row in user_data.iterrows():
        # If the username exists in csv, account exists
        if user == row["user"]:
            account_exists = True

    if account_exists:
        message = "User already exists"
    else:
        user_data = user_data.append({"user":user, "password": password}, ignore_index=True)
        user_data.to_csv(user_data_path, index_label = "id")
        message = "User successfully created"

    return message
