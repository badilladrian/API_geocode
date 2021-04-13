from models import Drone, User, HighSchool, Payload
from datetime import datetime
from utils import Utils
import pandas as pd
import os
from downloads.build_database import MongoDB
from street_viewer import StreetViewer
from urllib.parse import quote


class ControllerDrones:
    _drones = []
    def __init__(self):
        self.drones = []

    def get(self, drone_id):
        drone = self.look_drone(drone_id)
        return self.drones[position]

    def get_all(self):
        return self.drones

    def create(self):
        new_drone = Drone()
        self.drones.append(new_drone)
        return new_drone

    def update(self, drone: Drone):
        drone = self.modify_drone(drone)
        return True

    def look_drone(self, drone_id):
        drone_obj = [drone for drone in self.drones if drone.id == drone_id]
        return drone_obj


class ControllerUsers:
    _users = []
    def __init__(self):
        self.users = []

    def get(self, drone_id):
        drone = self.look_drone(drone_id)
        return self.users[position]

    def get_all(self):
        return self.users

    def create(self, new_user):
        new_user = User(new_user)
        self.users.append(new_user)
        return new_user

    def update(self, user: User):
        drone = self.modify_user(user)
        return True

    def look_user(self, uid):
        user_obj = [user for user in self.users if user.id == uid]
        return user_obj


class ControllerHighSchools:
    school_objs =[]    
    def __init__(self):
        self.school_objs = []
        
    def get(self, school_name):
        school = self.look_school(school_name)
        return self.high_schools[school]

    def get_all(self):
        return self.high_schools

    def look_school(self, school_name):
        school_obj = [school for school in self.high_schools if school.name == school_name]
        return school_obj

    def loadCollection(self):
        controllerMongo = ControllerMongo()
        data = controllerMongo.get_HS_objs()
        list_names = data['Name']
        list_addresses =data['Address']
        list_geocodes = data['Geocodes']
        list_latlon = []
        for record in list_geocodes:
            try:
                extract_geocodes = record.split(',') # ["{'lat': 41.7099492", " 'lng': -83.60549}"]
                extract_lat = extract_geocodes[0].split(':')
                lat = (extract_lat[1].strip())
                lat = float(lat)

                extract_lon = extract_geocodes[1].split(':')
                lon = (extract_lon[1].strip()) 
                if lon[-1] == '}':
                    lon = lon[:-1] 
                lon = float(lon)

                lat_lon_dic = {"lat": lat, "lon" : lon}
                list_latlon.append(dict(lat_lon_dic))
            except:
                print(type(extract_geocodes), extract_geocodes)
        for elem in range(0,len(list_latlon)):
            self.school_objs.append(HighSchool(name=list_names[elem], address=list_addresses[elem], geocodes=list_latlon[elem]))

class ControllerMongo:
    def __init__(self):
        self._mongodb = MongoDB()

    def get_HS_objs(self):
        cursor = self._mongodb._collection.find()
        mongo_docs = list(cursor)
        docs = pd.DataFrame(mongo_docs)
        docs.pop("_id")
        return docs


class ControllerPayload:
    payload_list = []
    def __init__(self):
        self.payload_list = []

    def get(self, payload_id):
        payload = self.look_payload(payload_id)
        return self.payload_list[payload]

    def get_all(self):
        return self.payload_list

    def create(self, args):
        payload = Payload()
        payload.create(args)
        self.payload_list.append(payload)
        return payload

    def update(self, payload: Payload):
        school = self.modify_user(school)
        return True

    def look_payload(self, school_name):
        school_obj = [school for school in self.high_schools if school.name == school_name]
        return school_obj

class ControllerAPI:
    solved_request = {}
    utils = {}
    controller_school = {}
    controller_drones = {}
    def __init__(self, *args):
        self.solved_request =  {}
        self.utils = Utils()
        self.controller_school = ControllerHighSchools()
        self.controller_drones = ControllerDrones()

    def run(self, lat, lon, uid):
        request =  {'lat':lat, 'lon':lon, 'uid': uid}
        self.solved_request = self.process_request(request)

    def process_request(self, request):
        user_location= {"lat":float(request['lat']), "lon":float(request['lon'])}
        self.controller_school.loadCollection()
        geocodes = [ school._geocodes for school in self.controller_school.school_objs]
        closest_gecodes = self.utils.closest(geocodes,user_location)
        miles_user_to_school = self.utils.miles_between(user_location, [str(closest_gecodes['lat']),
                                                                str(closest_gecodes['lon'])])
        winner_school = [ school for school in self.controller_school.school_objs if closest_gecodes==school._geocodes]
        data = [request, closest_gecodes, miles_user_to_school, winner_school[0]]
        result = self.create_result(data)

        return result

    def create_result(self, data): # import pdb; pdb.set_trance()
        user_geocodes = [data[0]['lat'], data[0]['lon']]
        school = data[3]
        distance = data[2]
        speed = (distance/80) * 60
        # street_view = StreetViewer(location=school._address)
        # meta = street_view.get_meta()
        # picture = street_view.get_pic()
        school_geocodes = self.utils.address_to_geocode(school._address)
        
        return (
                data[0]['uid'],
                user_geocodes,
                datetime.now(), 
                self.controller_drones.create(),
                '{} miles'.format(float(distance)),
                '{} minutes'.format(float(distance/speed)),
                '{} ml/h'.format(float(speed)),
                    {
                        "name": school._name,
                        "address": school._address, 
                        "geocodes": school_geocodes,  
                        "URL": quote(school._address)
                    },
                    self.utils.google_map_markers(user_geocodes, school_geocodes)
                )