import sqlite3
from tables import *
from flask import Flask, request, send_file, redirect

db = sqlite3.connect("data.db", check_same_thread=False)
app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if(not False):
        return redirect("login")
    return send_file("login.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    return send_file("login.html")

@app.route("/verf", methods = ['POST', 'GET'])
def verf():
    data = dict(request.form)
    if(("username" in data and "password" in data) == False):
        return "Username or password wrong"
    cur = db.execute(f"SELECT * FROM user WHERE password = '{data['password']}' AND username = '{data['username']}'")
    length = 0
    for i in cur:
        length += 1
    if(length != 0):
        return "Yes"
    else:
        return "No"

app.run(debug=True)
# db = sqlite3.connect("data.db")
# def menu():
#     for i in db.execute("SELECT * FROM sqlite_master WHERE type='table' AND name!='sqlite_sequence'"): print(i)
# menu()
# db.close()