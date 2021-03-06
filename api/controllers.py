from api.models import Drone, User, HighSchool, Payload
from datetime import datetime
from api.utils import Utils
import pandas as pd
import os
from api.build_database import MongoDB
from urllib.parse import quote

"""Controllers are to invoke CRUD operations at models eventually"""
"""They are not being fully used as there is no data-persistance
Last two controllers are super important """

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
    """ THIS ONE IS IMPORTANT, IT LOADS ALL SCHOOLS_OBJ FROM MONGO"""
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
        """ reads school collection, parse data as needed and appends HighSchool() to list self.school_obj  """
        controllerMongo = ControllerMongo()
        data = controllerMongo.retrieve_collection()
        list_names = data['Name']
        list_addresses =data['Address']
        list_geocodes = data['Geocodes']
        list_latlon = []
        for record in list_geocodes:
            try:
                extract_geocodes = record.split(',') # ["{'lat': 41.7099492", " 'lng': -83.60549}"] type(STR)
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

    def retrieve_collection(self):
        """ reads from schools collection, and takes off index"""
        cursor = self._mongodb._collection.find()
        mongo_docs = list(cursor)
        docs = pd.DataFrame(mongo_docs)
        docs.pop("_id")
        return docs


class ControllerAPI:
    """ executes the main processes and compose the response. Store it at self.solved_requests"""
    solved_request = {}
    utils = {}
    controller_school = {}
    controller_drones = {}
    def __init__(self, *args):
        self.utils = Utils() # all calculations and calls is in Utils
        self.solved_request =  {}
        self.controller_school = ControllerHighSchools()
        self.controller_drones = ControllerDrones()

    def run(self, lat, lon, uid): # requests params
        request =  {'lat':lat, 'lon':lon, 'uid': uid} # creates dict to pass it on in the pipeline process
        self.solved_request = self.process_request(request) # below method saves into self.attribute

    def process_request(self, request):
        """ creates list of schools, extract their geocodes into a list
        then use the haversine that recieves the list of school_geocodes vs. user_geolocation
        once it finds the closest school (it was only throu geocode) it looks for which school has those geocodes
        in the school_obj lists to retrieve all data [full Address, Name, Geocodes, image]* no image yet """

        user_location= { "lat": float(request['lat']), "lon": float(request['lon']) }

        self.controller_school.loadCollection()

        # schools_geocodes = [ ( float(school._geocodes['lat']), float(school._geocodes['lon']) ) for school in self.controller_school.school_objs]
        schools_geocodes = [ {'lat': float(school._geocodes['lat']), 'lon': float(school._geocodes['lon']) } for school in self.controller_school.school_objs]
        # school_geocode = self.utils.get_closest((float(request['lat']), float(request['lon'])), schools_geocodes)

        distances = []
        schools = []
        for school in schools_geocodes:
            miles_userlocation_to_school = self.utils.miles_between(user_location, school)
            distances.append(miles_userlocation_to_school)
            schools.append(school)
        closest_miles = min(distances)
        position = distances.index(closest_miles)
        winner_geocode = schools[position]

        winner_school = [ school for school in self.controller_school.school_objs if winner_geocode == school._geocodes]

                # list of result data to pass to start creating the response
        data = [request, closest_miles, miles_userlocation_to_school, winner_school[0]]

        result = self.create_result(data)

        return result

    def create_result(self, data):
        """ Creates a dict with all the values after process has  been finished to give to PAYLOAD obj"""
        user_geocodes = [data[0]['lat'], data[0]['lon']]
        school = data[3] 
        distance = data[1]
        speed = (distance/40) * 60   
        time = distance/speed
        if time > 2.0:
           for spd in range(40,80):
                speed = (distance/spd) * 60   
                time = distance/speed
                if time <= 2.0:
                    break
    
        flat_user_address = self.utils.address_from_geocode(user_geocodes)
        user_address = str(flat_user_address)
        return (
                data[0]['uid'],
                user_geocodes, # user geocodes from request
                user_address, # user address
                datetime.now(), #timestamp
                self.controller_drones.create(), # drone
                '{:.2f} miles'.format(float(distance)), # miles from user to drone [Drone are in HighSchools!]
                '{:.2f} minutes'.format(float(time)), # time will always be 1.3 minutes
                '{:.2f} ml/h'.format(float(speed)), # speed the drone needs to be to get in 1.3 minutes
                    { # school data 
                        "name": school._name,
                        "address": school._address, 
                        "geocodes": school._geocodes,  
                        "URL": quote(school._address)  # E.G. 301%20Melton%20Rd%2C%20Gary%2C%20IN%2046403%2C%20USA
                    },
                    # self.utils.google_map_markers(user_geocodes, school._geocodes)
                )
