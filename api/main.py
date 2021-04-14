import json
import flask
import datetime

from flask import request, jsonify
from flask_cors import CORS

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from utils import Utils
from cache import Cache
from controllers import ControllerHighSchools, ControllerAPI, ControllerMongo

# init API
app = flask.Flask(__name__)

# API configs
config = {
    "DEBUG": True,
    "JSON_SORT_KEYS": False
}

app.config.from_mapping(config)
                                        # TO ADD OPEN API DOCUMENTATION --- TASK # 5
# Init CORS
cors = CORS(app)

# Init to load all processes | controllers
controller_utils = Utils()
controller_payload = ControllerPayload()
controlller_schools = ControllerHighSchools()
controller_mongo = ControllerMongo()
controller_api = ControllerAPI()

#  _cache = Cache()      # IMPLEMENT CACHE | TASK # 4   This can be done as you wish- 
# I have a cache starting with JSONs As the obj response is a big payload (models.py Payload) -- all structures are in /static
# better to cache.json this objs in a JSON list- I encounter issues on how to save this files in proper format [ JSON1, JSON2, JSON3 ]
"""Cache Norms: If same user_geocodes at POST then return cache response.
If user_geocodes is between 2 miles ratio from store user_geocodes-cache answers:
respond any in range cache answer"""

@app.route('/', methods=['GET'])
def ping():
        return jsonify('Im active!')

@app.route('/debug-sentry')     # How to make sentry to work properly? TASK # 6
def trigger_error():    # badilladrianch@gmail.com  pass: pythonScorpion
    division_by_zero = 1 / 0

@app.route('/safewrd', methods=['POST'])
def user_location():
    try:
        geocodes = request_data['geocodes']   # [xx.xx,xx,xx]   --- [lat,lon]
        user_uid = request_data['uid']        # E.G. CA308008-421B-11EB-B2BF-EDEFCE1D72FE 
        # to add validations that geocodes are float & user_uid str
        lat, lon, uid = (geocodes[0], geocodes[1], user_uid)

        response = {}
        # response = _cache.get_cache(lat, lon, user_uid)  if same geocode makes request return cache request (to replace UID could be same, or new user)
        # response = _cache.between_two_miles(lat, lon, user_uid)   if user-geocodes from request is in 2 miles ratio of cache responses user-geocodes return cache  (to replace UID could be same, or new user)
        if response is None:  # if no cache
            controller_api.run(lat, lon, uid)  # regular process | run() makes calculations and store them at attribute ControllerApi.self.solved_request
            response = controller_payload.create(controller_api.solved_request) # reads this attribute and parse it to Payload obj | models.py
            # _cache.put_on_cache(response)   save new response in cache
        else:
           return response   # return cache response [that is in JSON format already]

        return jsonify(response.dic()) # return new response | Payload obj is not a JSONas a dic() [this is where maps are currently added]
    except:
        return jsonify('Error in request!')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000')  # TASK 1 DEPLOY AT SERVER W/ HTTPS + SSL ADDITION   -- uwsgi(?)

""" ssh root@104.236.59.158   
    pass JuicyFruit4y 
    cd /var/www/html/ """  # it already has ngix + certificates 
