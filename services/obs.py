import pandas as pd
from flask import jsonify
from services import connect
from services import aapl, fb, nflx, amzn

cur = connect.cursor
cur.execute("CREATE DATABASE IF NOT EXISTS accounts")
cur.execute("USE accounts")

# bank initialization at bottom

""" ACCOUNT MANAGEMENT """
# Add an account with starting $ for a user
def addAccount(userID, accountname, starting_balance):
    cur.execute("USE accounts")
    cur.execute("CREATE TABLE IF NOT EXISTS accounts(userid INTEGER NOT NULL, accountid INTEGER NOT NULL, accountname TEXT NOT NULL, funds DOUBLE NOT NULL, aapl INTEGER NOT NULL, fb INTEGER NOT NULL, nflx INTEGER NOT NULL, amzn INTEGER NOT NULL, created_at TEXT NOT NULL)")
    cur.execute("SELECT COUNT(*) FROM accounts")
    num_accounts = cur.fetchone()[0]
    cur.execute("INSERT INTO accounts(userid, accountid, accountname, funds, aapl, fb, nflx, amzn, created_at) VALUES ({},{},'{}',{},0,0,0,0,NOW())".format(userID,num_accounts,accountname,starting_balance))
    return 1

# View balance for a given account
def viewAccountBalance(account):
    return 1

""" TRANSACTIONS """
# Add money to a given account
def addFunds(accountid, added_funds):
    cur.execute("USE accounts")
    cur.execute("SELECT funds FROM accounts WHERE accountid = {}".format(accountid))
    current_funds = cur.fetchone()[0]
    new_funds = float(current_funds) + float(added_funds)
    cur.execute("UPDATE accounts SET funds = {} WHERE accountid = {}".format(new_funds, accountid))  

# Buy an amount of shares of a certain ticker for an account
def buyShares(account, ticker, amount):
    if ticker == "aapl":
        aapl.buy(amount, account)
    elif ticker == "fb":
        fb.buy(amount, account)
    elif ticker == "amzn":
        amzn.buy(amount, account)
    elif ticker == "nflx":
        nflx.buy(amount, account)


# Sell an amount of shares of a certain ticker for an account
def sellShares(account, ticker, amount):
    if ticker == "aapl":
        aapl.sell(amount, account)
    elif ticker == "fb":
        fb.sell(amount, account)
    elif ticker == "amzn":
        amzn.sell(amount, account)
    elif ticker == "nflx":
        nflx.sell(amount, account)

""" NET WORTH """
# Get total account balances and shares owned
def netWorth(user):
    return 1

""" DEBUG """
def viewAccounts():
    cur.execute("USE accounts")
    cur.execute("CREATE TABLE IF NOT EXISTS accounts(userid INTEGER NOT NULL, accountid INTEGER NOT NULL, accountname TEXT NOT NULL, funds DOUBLE NOT NULL, aapl INTEGER NOT NULL, fb INTEGER NOT NULL, nflx INTEGER NOT NULL, amzn INTEGER NOT NULL, created_at TEXT NOT NULL)")
    cur.execute("SELECT * FROM accounts")
    row_headers = [x[0] for x in cur.description]
    results = cur.fetchall()
    data = []
    for result in results:
        data.append(dict(zip(row_headers,result)))
    return data

# start bank off
if len(viewAccounts())==0:
    addAccount(0, "Bank", 10000000)
    for ticker in ("aapl", "amzn", "fb", "nflx"):
        buyShares(0, ticker, 5000)