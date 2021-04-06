class Drone:
    def __init__(self, _id):
        self._id = _id
        # self increment 

    def update(self, data):
        if data.id:
            self._id = data.id
        if data.speed:
            self._speed = data.speed


class User:
    def __init__(self, username):
        self._username = username
        self._geocode = [0.0,
                        0.0] 

    def update(self, data):
        if data.username:
            self._username = data.username
        if data.geocode:
            self._speed = data.geocode


class HighSchool:
    def __init__(self, name, address):
        self._name = name
        self._address = address
        self._image = False
        self._geocode = [0.0,
                        0.0] 

    def update(self, data):
        if data.name:
            self._name = name
        if data.speed:
          self._address = address
