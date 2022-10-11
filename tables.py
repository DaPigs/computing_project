class Permission:
    def __init__(self, *args):
        self.id, self.room_id, self.user_id, self.permission_level = args

class Point:
    def __init__(self, *args):
        self.id, self.point = args

class Room:
    def __init__(self, *args):
        self.id, self.description = args

class Room_User:
    def __init__(self, *args):
        self.id, self.room_id = args

class User:
    def __init__(self, *args):
        self.id, self.pic, self.username, self.password = args