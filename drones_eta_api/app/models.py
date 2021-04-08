import json
import random
import string
import datetime
import itertools
from json import JSONEncoder

class Drone:
    id_iter = itertools.count()
    def __init__(self):
        self.id_iter = next(Drone.id_iter)

    def update(self, data):
        if data.id:
            self._id = data.id
        if data.speed:
            self._speed = data.speed


class User:
    def __init__(self, username):
        self._uid = _uid
        self._geocode = [0.0,
                        0.0] 

    def update(self, data):
        if data.uid:
            self._uid = data._uid
        if data.geocode:
            self.geocode = data.geocode


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

class Payload(object):
    payload = {}
    id_iter = itertools.count()
    def __init__(self, args):
        self.id_iter = next(Payload.id_iter)
        self.payload =   {
                    "user_data": args[1], 
                    "date_of_request": args[0].strftime("%m/%d/%Y, %H:%M:%S"), 
                    "payload_id": self.id_iter ,
                    "drone": { 
                            "drone_id" : args[2], 
                            "drone_speed" :  args[4],
                            },
                    "miles_distance":  args[3], 
                    "estimated_time":  args[5], 
                    "embedded_map": ["<iframe width=","600"," height=","500"," id=","gmap_canvas",
                        "src=", "https://maps.google.com/maps?q=san%20miguel%20santo%20domingo&t=&z=13&ie=UTF8&iwloc=&output=embed",
                        "frameborder=", "0"," scrolling=","no"," marginheight=","0"," marginwidth=","0","></iframe>"],                
                    "nearest_school":
                                {
                                "address": args[6]['address'], 
                                "geocodes": args[6]['geocodes'],    
                                "school_image": "https://artsandculture.google.com/asset/son-doong-cave-31-ryan-deboodt/YwEz2BEy3rWHtw",
                                },
                    "airgeos_vote_url": "https://www.aireos.io/network/"
            }
        self.json = Encoder().encode(self.payload)

    def __str__(self):
        print(self.json)


    def generate_id(self, id_ctr):
        caracters = string.ascii_letters + string.digits 
        add_unique_value = ''.join(random.choice(caracters) for i in range(8))
        return '{}_safewrd_{}'.format(id_ctr, add_unique_value)



class Encoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
