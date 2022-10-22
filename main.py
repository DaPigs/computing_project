import sqlite3
from tables import *
from flask import Flask, request, send_file, redirect, make_response, render_template, url_for
import os

db = sqlite3.connect("data.db", check_same_thread=False)
app = Flask("scores", template_folder=os.getcwd())

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
    return redirect(url_for("rooms"))

@app.route("/update_profile/", methods = ['POST', 'GET'])
def update_profile():
    if (not logged_in()):
        return redirect(url_for("login"))
    user = get_user()
    data = dict(request.form)
    cur = sql(f"SELECT * FROM user WHERE username = \"{data['username']}\"")
    if(len(cur) == 0):
        sql(f"UPDATE user SET username = \"{data['username']}\" WHERE id = {user.id}")
        data["username"] = "Username updated"
    else:
        newuser = User(*cur[0])
        if(newuser.username == user.username):
            data["username"] = "Username updated"
            pass
        else:
            data["username"] = "Username in use"
    if(data["old-pw"] == ""):
        data["old-pw"] = "Password did not update"
        data["new-pw"] = "Password did not update"
        data["confirm-pw"] = "Password did not update"
    elif(data["old-pw"] != user.password):
        data["old-pw"] = "Wrong Password"
        data["new-pw"] = "Wrong old Password"
        data["confirm-pw"] = "Wrong old Password"
    else:
        data["old-pw"] = "Correct Password"
        if(data["new-pw"] == data["confirm-pw"]):
            sql(f"UPDATE user SET password = \"{data['new-pw']}\" WHERE id = {user.id}")
            data["new-pw"] = "Password changed"
            data["confirm-pw"] = "Password changed"
        else:
            data["new-pw"] = ""
            data["confirm-pw"] = "Confirmed password differs from new password"
    sql(f"UPDATE user SET pic = \"{data['pic']}\" WHERE id = {user.id}")
    data["pic"] = "Profile picture URL updated"
    S = """
<script>
window.addEventListener("DOMContentLoaded", () => {
  fetch("/header.html")
      .then((res) => res.text())
      .then((html) => {
        document.body.insertAdjacentHTML("afterbegin", html);
        navbarInit();
      });
});
</script>
"""
    for i in data:
        S += f"{i}: {data[i]}<br>"
    return S

@app.route("/profile/", methods = ['POST', 'GET'])
def profile():
    if(not logged_in()):
        return redirect(url_for("login"))
    user = get_user()
    return render_template("profile.html", user=user)

@app.route("/manage/<room>", methods = ['POST', 'GET'])
def manage(room):
    if(not logged_in()):
        return redirect(url_for("login"))

    cur = sql(f"SELECT * FROM room WHERE id = {room}")
    room = Room(*cur[0])

    cur = sql(f"SELECT [Room-User].id, [Room-User].room_id, [Room-User].user_id, nickname FROM [Room-User], Permission WHERE Permission.room_id = [Room-User].room_id AND Permission.permission_level = 5 AND Permission.room_id = {room.id}")
    owner = Room_User(*cur[0])

    cur = sql(f"SELECT [room-user].id, [room-user].room_id, [room-user].user_id, [room-user].nickname, Permission.permission_level, SUM(point.point) FROM [room-user], Permission, Point WHERE Permission.room_id = {room.id} AND [room-user].room_id = {room.id} AND Permission.user_id = [room-user].user_id AND point.id = [room-user].id GROUP BY point.id ORDER BY Permission.permission_level DESC")

    permissions = []
    for i in cur:
        permissions.append({
            "id": i[0],
            "room_id": i[1],
            "user_id": i[2],
            "nickname": i[3],
            "permission_level": i[4],
            "points": i[5]
        })
    return render_template("manage.html", permissions=permissions, room=room, owner=owner, user=get_user())

@app.route("/ownership/<room>/<uid>", methods = ['POST', 'GET'])
def ownership(room, uid):
    if (not logged_in()):
        return redirect(url_for("login"))
    user = get_user()
    cur = sql(f"SELECT * FROM Permission WHERE room_id = {room} AND user_id = {user.id}")
    permission = Permission(*cur[0])
    if(permission.permission_level == 5):
        cur = sql(f"SELECT * FROM Permission WHERE room_id = {room} AND user_id = {uid}")
        if(len(cur)):
            sql(f"UPDATE Permission SET permission_level = 5 WHERE user_id = {uid}")
            sql(f"UPDATE Permission SET permission_level = 4 WHERE user_id = {user.id}")
    return redirect(url_for("rooms"))

@app.route("/update/<room>", methods = ['POST', 'GET'])
def update(room):
    if (not logged_in()):
        return redirect(url_for("login"))
    user = get_user()
    cur = sql(f"SELECT * FROM Permission WHERE room_id = {room} AND user_id = {user.id}")
    permission = Permission(*cur[0])
    if(permission.permission_level not in [5,4,3,2]):
        return redirect(url_for("rooms"))
    data = dict(request.form)
    for i in data:
        action, uid = i.split("-")
        if(action == "user"):
            sql(f"UPDATE [room-user] SET nickname = \"{data[i]}\" WHERE user_id = {user.id} AND room_id = {room}")
            continue
        if(action == "room"):
            cur = sql(f"SELECT * FROM Permission WHERE room_id = {room} AND user_id = {user.id}")
            p = Permission(*cur[0])
            if(p.permission_level in [4,5]):
                if(uid == "name"):
                    sql(f"UPDATE Room SET name = \"{data[i]}\" WHERE id = {room}")
                if(uid == "description"):
                    sql(f"UPDATE Room SET description = \"{data[i]}\" WHERE id = {room}")
            continue
        value = int(data[i])
        if(action == "permission_level"):
            cur = sql(f"SELECT * FROM [room-user] WHERE room_id = {room} AND user_id = {uid}")
            if (len(cur)):
                cur = sql(f"SELECT * FROM Permission WHERE room_id = {room} AND user_id = {uid}")
                p = Permission(*cur[0])
                if(value < permission.permission_level and value >= 1 and p.permission_level < permission.permission_level):
                    sql(f"UPDATE Permission SET permission_level = {value} WHERE user_id = {uid}")
        if(action == "points"):
            if(permission.permission_level > 1):
                cur = sql(f"SELECT * FROM [room-user] WHERE room_id = {room} AND user_id = {uid}")
                if(len(cur)):
                    room_user = Room_User(*cur[0])
                    sql(f"INSERT INTO point (id, point) VALUES ({room_user.id}, {value})")
    return redirect(url_for("rooms"))

@app.route("/join", methods = ['POST', 'GET'])
def join():
    if(not logged_in()):
        return redirect(url_for("login"))
    user = get_user()
    data = dict(request.form)
    if("room_id" in data == False):
        raise SystemError

    cur = sql(f"SELECT * FROM room WHERE id = {data['room_id']}")
    room = Room(*cur[0])

    sql(f"INSERT INTO [room-user] (room_id, user_id, nickname) VALUES ({room.id}, {user.id}, {user.username})")

    cur = sql(f"SELECT * FROM [room-user] WHERE room_id = {room.id} AND user_id = {user.id}")
    room_user = Room_User(*cur[0])

    sql(f"INSERT INTO permission (room_id, user_id, permission_level) VALUES ({room.id}, {user.id}, 1)")

    sql(f"INSERT INTO point (id, point) VALUES ({room_user.id}, 0)")

    return redirect(url_for("rooms"))

@app.route("/leaderboard/<room>", methods = ['POST', 'GET'])
def leaderboard(room):
    if(not logged_in()):
        return redirect(url_for("login"))

    cur = sql(f"SELECT [Room-User].id, [Room-User].room_id, [Room-User].user_id, nickname FROM [Room-User], Permission WHERE Permission.room_id = [Room-User].room_id AND Permission.permission_level = 5 AND Permission.room_id = {room}")
    owner = Room_User(*cur[0])

    cur = sql(f"SELECT [Room-User].nickname, SUM(Point.point) AS points FROM [Room-User], Point WHERE [Room-User].id = Point.id AND [Room-User].room_id = {room} GROUP BY Point.id ORDER BY points DESC")
    ranks = []
    counter = 1
    for i in cur:
        ranks.append({
            "rank": str(counter),
            "nickname": i[0],
            "points": i[1]
        })
        counter += 1
    return render_template("leaderboard.html", ranks=ranks, room=room, owner=owner)

@app.route("/create_room", methods = ['POST', 'GET'])
def create_room():
    if(not logged_in()):
        return redirect(url_for("login"))
    user = get_user()

    sql(f"INSERT INTO Room (name) VALUES (NULL)")
    cur = sql(f"SELECT * FROM room ORDER BY id DESC")
    room = Room(*cur[0])

    sql(f"INSERT INTO [room-user] (room_id, user_id) VALUES ({room.id}, {user.id})")

    cur = sql(f"SELECT * FROM [room-user] WHERE room_id = {room.id} AND user_id = {user.id}")
    room_user = Room_User(*cur[0])

    sql(f"INSERT INTO permission (room_id, user_id, permission_level) VALUES ({room.id}, {user.id}, 5)")

    sql(f"INSERT INTO point (id, point) VALUES ({room_user.id}, 0)")

    return redirect(url_for("rooms"))

@app.route("/room/<room>", methods = ['POST', 'GET'])
def room(room):
    if(not logged_in()):
        return redirect(url_for("login"))
    user = get_user()

    cur = sql(f"SELECT * FROM room WHERE id = {room}")
    room = Room(*cur[0])

    cur = sql(f"SELECT * FROM [Room-User] WHERE user_id = {user.id}")
    room_user = Room_User(*cur[0])

    cur = sql(f"SELECT [Room-User].id, [Room-User].room_id, [Room-User].user_id, nickname FROM [Room-User], Permission WHERE Permission.room_id = [Room-User].room_id AND Permission.permission_level = 5 AND Permission.room_id = {room.id}")
    owner = Room_User(*cur[0])

    cur = sql(f"SELECT id, SUM(point) FROM point WHERE id = {room_user.id}")
    point = Point(*cur[0])

    return render_template("room.html", owner=owner, room=room, user=user, room_user=room_user, point=point)

@app.route("/rooms", methods = ['POST', 'GET'])
def rooms():
    if(not logged_in()):
        return redirect(url_for("login"))
    uid = request.cookies.get('uid')
    cur = sql(f"SELECT room.id, room.description, room.name FROM room, [Room-User] WHERE room.id = [Room-User].room_id AND [Room-User].user_id = {uid}")
    for i in range(len(cur)):
        cur[i] = Room(*cur[i])
    return render_template("rooms.html", rooms=cur)

@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    return send_file("signup.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    return send_file("login.html")

@app.route("/logout", methods = ['POST', 'GET'])
def logout():
    resp = make_response(redirect(url_for("rooms")))
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
    sql(f"INSERT INTO user (username, password) VALUES (\"{data['username']}\", \"{data['password']}\")")
    return redirect(url_for("login"))

@app.route("/verf", methods = ['POST', 'GET'])
def verf():
    data = dict(request.form)
    if(("username" in data and "password" in data) == False):
        return "Wrong username/password <a href='login'>Go back</a>"
    cur = sql(f"SELECT * FROM user WHERE password = '{data['password']}' AND username = '{data['username']}'")
    if(len(cur) == 1):
        user = User(*cur[0])
        resp = make_response(redirect(url_for("rooms")))
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