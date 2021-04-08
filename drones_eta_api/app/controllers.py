from models import Drone, User, HighSchool, Payload
from datetime import datetime
from utils import Utils

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
    high_schools =[]    
    def __init__(self):
        school_1 = {'lat': 40.712776, 'lon': -74.005974}
        school_2 = {'lat': 47.751076,  'lon': -120.740135}
        school_3 = {'lat': 37.774929, 'lon': -122.419418}        
        self.high_schools = [school_1, school_2, school_3]
        
    def get(self, school_name):
        school = self.look_school(school_name)
        return self.high_schools[school]

    def get_all(self):
        return self.high_schools

    def create(self, new_school):
        new_school = User(new_user)
        self.high_schools.append(new_school)
        return new_school

    def update(self, school: User):
        school = self.modify_user(school)
        return True

    def look_school(self, school_name):
        school_obj = [school for school in self.high_schools if school.name == school_name]
        return school_obj

class ControllerMongo:
    connection_string = ''
    def __init__(self):
        self.connection_string =  ''

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
        payload = Payload(args)
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
        user_location= [request['lat'], request['lon']]
        closest_gecodes = self.utils.closest(self.controller_school.high_schools,
                                                {'lat':float(user_location[0]),'lon':float(user_location[1])})

        miles_user_to_school = self.utils.miles_between(user_location, [str(closest_gecodes['lat']),
                                                                str(closest_gecodes['lon'])])

        data = (request, closest_gecodes, miles_user_to_school)
        result = self.create_result(data)

        return result

    def create_result(self, data): # import pdb; pdb.set_trance()
        geocodes = [data[0]['lat'], data[0]['lon']]
        distance = data[2]
        time = (distance/80) * 60
        return (
                data[0]['uid'],
                datetime.now(), 
                self.controller_drones.create(),
                float(distance),
                float(distance/time),
                float(time),
                    {
                        "address": self.utils.geocode_to_address(data[1]), 
                        "geocodes": data[1],  
                        "image": self.utils.street_view_school(data[1])
                    },
                )