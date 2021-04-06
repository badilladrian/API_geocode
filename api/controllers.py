from models import Drone, User, HighSchool

class ControllerDrones:
    drones = []
    drones_ids = []

    def get(self, id: int):
        position = self._drones_ids.index(id)
        return self._drones[position]

    def get_all(self):
        return self._drones

    def create(self, drone_id):
        new_drone = Drone(drone_id)
        self._drones.append(new_drone)
        return True

    def update(self, drone: Drone):
        pass


class ControllerUsers:
    users = []
    usernames = []


    def get(self, username: str):
        position = self._usernames.index(username)
        return self._users[position]

    def get_all(self):
        return self._users

    def create(self, username):
        new_user = User(username)
        self._users.append(new_user)
        return True

    def update(self):
        pass


class ControllerHighSchools:
    high_schools = []


class ControllerDatabase:
    connection_string = ''
