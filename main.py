import sqlite3

class Permission:
    def __init__(self, *args):
        self.id, self.room_id, self.user_id, self.permission_level = args

class Point:
    def __init__(self, *args):
        self.id, self.point = args

class Room:
    def __init__(self, *args):
        self.id, self.description = args

class Room-User:
    def __init__(self, *args):
        self.id, self.room_id = args

db = sqlite3.connect("data.db")
cur = db.execute("SELECT * FROM user")
for i in cur:
    print(i)

db.close()