class Permission:
    def __init__(self, *args):
        self.id, self.room_id, self.user_id, self.permission_level = args
        self.args = args

    def __str__(self):
        return str(self.args)

class Point:
    def __init__(self, *args):
        self.id, self.point = args
        self.args = args

    def __str__(self):
        return str(self.args)

class Room:
    def __init__(self, *args):
        self.id, self.description, self.name = args
        self.args = args

    def __str__(self):
        return str(self.args)

class Room_User:
    def __init__(self, *args):
        self.id, self.room_id = args
        self.args = args

    def __str__(self):
        return str(self.args)

class User:
    def __init__(self, *args):
        self.id, self.pic, self.username, self.password = args
        self.args = args

    def __str__(self):
        return str(self.args)