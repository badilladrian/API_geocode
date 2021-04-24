import json
import flask
import datetime

from flask import request, jsonify
from flask_cors import CORS

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from api.models import Payload
from api.utils import Utils
# from cache import Cache 
from api.controllers import ControllerHighSchools, ControllerAPI, ControllerMongo

app = flask.Flask(__name__)

config = {
    "DEBUG": True,
    "JSON_SORT_KEYS": False
}

app.config.from_mapping(config)
cors = CORS(app)

controller_utils = Utils()
controller_api = ControllerAPI()

#  _cache = Cache() <--  OBJ

# END POINTS 
@app.route('/', methods=['GET'])
def ping():
        return jsonify('Im active!')


@app.route('/debug-sentry')                   
def trigger_error():                          
    division_by_zero = 1 / 0


@app.route('/safewrd', methods=['POST'])
def user_location():
    data = request.get_json()
    geocodes = data['geocodes']  
    user_uid = data['uid']     
    lat, lon, uid = (geocodes[0], geocodes[1], user_uid)
    response = {}

    # cache logic  TASK#--4   This can be done as you wish-
    # response = _cache.get_cache(lat, lon, user_uid)  if same geocode makes request return cache request (to replace UID as could be same or new user)
    # response = _cache.between_two_miles(lat, lon, user_uid)   if user-geocodes request is in 2 miles from cache user-geocodes responses return same response  (to replace UID as could be same or new user)

    # if no cache then
    if response == {}:           
        controller_api.run(lat, lon, uid)  # run stores result 
        args = controller_api.solved_request # at ControllerApi.self.solved_request

        payload = Payload()
        payload.create(args)            
        response = payload.parse()
        # _cache.put_on_cache(response)  this works <-- E.G. cache/cache.json it is incomplete TASK#--3 Write, Read, Load cache JSONs 
    else:
        return response 

    return jsonify(response) 


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000')  
    
