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
        user , geocodes, user_address, timestamp, drone, miles, speed, eta_time, school_dict = args
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
        iframe = "https://www.google.com/maps/embed/v1/directions?key=AIzaSyDyn3nhSkxdxS6aUJXim4O-T50ZtLg4YGY&origin={}&destination={}".format(self.args[2], self.args[8]['URL'])
        self.payload =   {
                    "user_data": str(self.args[0]),  # uid
                    "user_location": self.args[1],  # user_geocodes 
                    "user_address": self.args[2],
                    "date_of_request": str(self.args[3]),  # time stamp
                    "payload_id": self.generate_unique_id(self.id_iter), # auto-increment payload id
                    "drone": { 
                            "drone_id" : self.args[4].id_iter, # auto-increment drone id
                            "drone_speed" :  self.args[7], # drone speed
                            },
                    "miles_distance":  self.args[5], # distance between userlocation closest schoool
                    "estimated_time":  self.args[6], # always 1.3 minutes
                    "embedded_map": "iframe",  # iFrame with school marker
                    "nearest_school": {
                                "name": self.args[8]['name'],
                                "address": self.args[8]['address'], 
                                "geocodes": self.args[8]['geocodes'],
                                "school_image": 'https://maps.googleapis.com/maps/api/streetview?size=800x600&location={}&key=AIzaSyDyn3nhSkxdxS6aUJXim4O-T50ZtLg4YGY' \
                                    .format(self.args[8]['URL'])
                    },                                                 
                    "aireos_vote_url": "https://www.aireos.io/network/"
            }      
        return self.payload


