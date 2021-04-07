from models import Drone, User, HighSchool

class ControllerDrones:
    drones = []
    dronesIds = []

    def get(self, id: int):
        posCition = self.dronesIds.index(id)
        return self.drones[position]

    def get_all(self):
        return self.drones

    def create(self, droneId):
        newDrone = Drone(droneId)
        self.drones.append(newDrone)
        return True

    def update(self, drone: Drone):
        pass


class ControllerUsers:
    users = []
    userNames = []


    def get(self, userName: str):
        position = self._userNames.index(userName)
        return self._users[position]

    def get_all(self):
        return self._users

    def create(self, userName):
        newUser = User(userName)
        self._users.append(newUser)
        return True

    def update(self):
        pass


class ControllerHighSchools:
    highSchools = []


class ControllerDatabase:
    connectionString = ''
