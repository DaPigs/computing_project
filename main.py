import sqlite3
from tables import *
from flask import Flask, request, send_file, redirect, make_response
import os

db = sqlite3.connect("data.db", check_same_thread=False)
app = Flask("scores")

def sql(S):
    cur = db.execute(S)
    db.commit()
    return cur.fetchall()

def get_user():
    cur = sql(f"SELECT * FROM user WHERE id = {request.cookies.get('uid')}")
    user = User(*cur[0])
    return user

def logged_in():
    uid = request.cookies.get('uid')
    if(uid == None):
        return False
    cur = sql(f"SELECT * FROM user WHERE id = {uid}")
    if(len(cur) == 1):
        return True
    else:
        return False

def text(name):
    f = open(name, "r", encoding="utf8")
    S = f.read()
    f.close()
    return S

@app.route("/", methods = ['POST', 'GET'])
def index():
    return redirect("rooms")

@app.route("/room/<room>", methods = ['POST', 'GET'])
def room(room):
    if(not logged_in()):
        return redirect("login")
    cur = sql(f"SELECT * FROM room WHERE id = {room}")
    room = Room(*cur[0])
    return f"""
<form action="../rooms">
    <input type="submit" value="Back" />
</form>
<table border=\"1\">
    <tr>
        <th>Room name</th>
        <th>Room description</th>
        <th>Enter room</th>
    </tr>
    <tr>
        <td>{room.name}</td>
        <td>{room.description}</td>
        <td><form action="../room/{room.id}">
            <input type="submit" value="Enter" />
        </form></td>
    </tr>
</table>"""

@app.route("/rooms", methods = ['POST', 'GET'])
def rooms():
    if(not logged_in()):
        return redirect("login")
    uid = request.cookies.get('uid')
    S = text("rooms.html")
    cur = sql(f"SELECT room.id, room.description, room.name FROM room, [Room-User] WHERE room.id = [Room-User].room_id AND [Room-User].user_id = {uid}")
    for i in range(len(cur)):
        cur[i] = Room(*cur[i])

    for i in cur:
        S += f"""
<tr>
    <td>{i.name}</td>
    <td>{i.description}</td>
    <td><form action="../room/{i.id}">
        <input type="submit" value="Enter" />
    </form></td>
</tr>"""

    S += "</table>"
    return S

@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    return send_file("signup.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    return send_file("login.html")

@app.route("/logout", methods = ['POST', 'GET'])
def logout():
    resp = make_response(redirect("rooms"))
    resp.set_cookie('uid', '0', expires=0)
    return resp

@app.route("/create_account", methods = ['POST', 'GET'])
def create_account():
    data = dict(request.form)
    if(("username" in data and "password" in data) == False):
        return "Username or password wrong"
    cur = sql(f"SELECT * FROM user WHERE username = '{data['username']}'")
    if(len(cur)):
        return "Username already in use"
    sql(f"INSERT INTO user (username, password) VALUES ('{data['username']}', '{data['password']}')")
    return redirect("login")

@app.route("/verf", methods = ['POST', 'GET'])
def verf():
    data = dict(request.form)
    if(("username" in data and "password" in data) == False):
        return "Wrong username/password <a href='login'>Go back</a>"
    cur = sql(f"SELECT * FROM user WHERE password = '{data['password']}' AND username = '{data['username']}'")
    if(len(cur) == 1):
        user = User(*cur[0])
        resp = make_response(redirect("rooms"))
        resp.set_cookie('uid', str(user.id))
        return resp
    else:
        return "Wrong username/password <a href='login'>Go back</a>"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return send_file(path)

app.secret_key = os.urandom(24)
app.run()