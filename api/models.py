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
    def __init__(self, userName):
        self._userName = userName
        self._geoCode = [0.0,
                        0.0] 

    def update(self, data):
        if data.userName:
            self._userName = data.userName
        if data.geoCode:
            self._geoCode = data.geoCode #GFM


class HighSchool:
    def __init__(self, name, address):
        self._name = name
        self._address = address
        self._image = False
        self._geocode = [0.0,
                        0.0] 

    def update(self, data):
        if data.name:
            self._name = data.name #GFM
        if data.speed:
          self._address = data.address #GFM
