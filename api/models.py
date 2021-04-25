import json
import random
import string
import itertools
import shortuuid
from datetime import datetime


class Drone:
    id_iter = itertools.count()
    speed = 0
    id_iter = itertools.count() 
    def __init__(self):
        self.id_iter = next(Drone.id_iter)
        self.speed = 0


class User:
    def __init__(self, _uid, lat, lon):
        self._uid = _uid
        self._geocode = [lat,
                           lon] 

class HighSchool:
    def __init__(self, name, address, geocodes):
        self._name = name
        self._address = address
        self._id = shortuuid.uuid()
        self._geocodes = geocodes


class Payload(object):
    payload = {}
    id_iter = itertools.count()
    def __init__(self):
        self.id_iter = next(Payload.id_iter)
        self.payload = {}
        self.args = []

    def generate_unique_id(self, id_ctr):
        caracters = string.ascii_letters + string.digits 
        add_unique_value = ''.join(random.choice(caracters) for i in range(8))
        return '{}_safewrd_{}'.format(id_ctr, add_unique_value)
        
    def create(self,args):
        user , geocodes, timestamp, drone, miles, speed, eta_time, school_dict, size = args
        self.args = args

        self.payload =   {
                            "user_data": user, 
                            "user_location": geocodes,
                            "date_of_request": str(timestamp), 
                            "payload_id": self.id_iter ,
                            "drone": { 
                                    "drone_id" : drone.id_iter, 
                                    "drone_speed" : speed,
                                    },
                            "miles_distance":  miles, 
                            "estimated_time":  eta_time, 
                            "embedded_map": 'NA', 
                            "nearest_school":
                                        {
                                        "name": school_dict['name'],
                                        "address": school_dict['address'], 
                                        "geocodes": school_dict['geocodes'],    
                                        "school_image":  school_dict['URL'], 
                                        },
                            "aireos_vote_url": "https://www.aireos.io/network/"
                    }



    def parse(self):
        iframe = """<iframe width="600" height="500" id="gmap_canvas" src="https://maps.google.com/maps?q={}&t=&z=13&ie=UTF8&iwloc=&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>""".format(self.args[7]['URL'])
        self.payload =   {
                    "user_data": str(self.args[0]),  # uid
                    "user_location": self.args[1],  # user_geocodes 
                    "date_of_request": str(self.args[2]),  # time stamp
                    "payload_id": self.generate_unique_id(self.id_iter), # auto-increment payload id
                    "drone": { 
                            "drone_id" : self.args[3].id_iter, # auto-increment drone id
                            "drone_speed" :  self.args[6], # drone speed
                            },
                    "miles_distance":  self.args[4], # distance between userlocation closest schoool
                    "estimated_time":  self.args[5], # always 1.3 minutes
                    "embedded_map": iframe,  # iFrame with school marker
                    "nearest_school": {
                                "name": self.args[7]['name'],
                                "address": self.args[7]['address'], 
                                "geocodes": self.args[7]['geocodes'],
                                "school_image": 'https://maps.googleapis.com/maps/api/streetview?size={}&location={}&key=AIzaSyDyn3nhSkxdxS6aUJXim4O-T50ZtLg4YGY'.format(self.args[8], self.args[7]['URL'])
                    },                                                 
                    "aireos_vote_url": "https://www.aireos.io/network/"
            }      
        return self.payload


