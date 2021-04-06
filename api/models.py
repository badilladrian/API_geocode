class Drone:
    self._id = ''
    self._speed = int()

    def __init__(self, _id):
        self._id = _id

    def update(self, data):
        if data.id:
            self._id = data.id
        if data.speed:
            self._speed = data.speed


class User:
    self._username = ''
    self._geocode = [0.0,
                    0.0] 

    def __init__(self, _username):
        self._username = _username

    def update(self, data):
        if data.username:
            self._username = data.username
        if data.geocode:
            self._speed = data.geocode


class HighSchool:
    self._name = ''
    self._address = ''
    self._image = False
    self._geocode = [0.0,
                    0.0] 

    def __init__(self, name, address):
        self._name = name
        self._address = address

    def update(self, data):
        if data.name:
            self._name = name
        if data.speed:
          self._address = address
