class Permission:
    def __init__(self, *args):
        self.id, self.room_id, self.user_id, self.permission_level = args
        self.args = args

    def __str__(self):
        return f'id:{self.id}\nroom_id:{self.room_id}\nuser_id:{self.user_id}\npermission_level:{self.permission_level}'

    items = ['id,' 'room_id,' 'user_id,' 'permission_level,']

class Point:
    def __init__(self, *args):
        self.id, self.point = args
        self.args = args

    def __str__(self):
        return f'id:{self.id}\npoint:{self.point}'

    items = ['id,' 'point,']

class Room:
    def __init__(self, *args):
        self.id, self.description, self.name = args
        self.args = args

    def __str__(self):
        return f'id:{self.id}\ndescription:{self.description}\nname:{self.name}'

    items = ['id,' 'description,' 'name,']

class Room_User:
    def __init__(self, *args):
        self.id, self.room_id, self.user_id, self.nickname = args
        self.args = args

    def __str__(self):
        return f'id:{self.id}\nroom_id:{self.room_id}\nuser_id:{self.user_id}\nnickname:{self.nickname}'

    items = ['id,' 'room_id,' 'user_id,' 'nickname,']

class User:
    def __init__(self, *args):
        self.id, self.pic, self.username, self.password = args
        self.args = args

    def __str__(self):
        return f'id:{self.id}\npic:{self.pic}\nusername:{self.username}\npassword:{self.password}'

    items = ['id,' 'pic,' 'username,' 'password,']

table_dict = {'permission': Permission, 'point': Point, 'room': Room, 'room_user': Room_User, 'user': User}