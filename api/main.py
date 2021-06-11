import json
import flask
import datetime
import os
import redis

from flask import request, jsonify, make_response
from flask_cors import CORS, cross_origin
from flask_caching import Cache

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from api.models import Payload
from api.utils import Utils
from api.controllers import ControllerAPI, ControllerDrones
from utils.store_image import StoreImage
import logging

logger = logging.getLogger(__name__)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = flask.Flask(__name__)
redis_instance = redis.Redis()

config = {
    "DEBUG": True,
    "JSON_SORT_KEYS": False
}

cache_config = {
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'server1',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': '6379',
    'CACHE_REDIS_URL': 'redis://localhost:6379'
}

app.config.from_mapping(config)
app.config.from_mapping(cache_config)
cache = Cache(app)
# TO ADD OPEN API DOCUMENTATION --- TASK#--5
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

controller_utils = Utils()
controller_api = ControllerAPI()
controller_drones = ControllerDrones()


#  _cache = Cache() <--  OBJ

# END POINTS 
@app.route('/', methods=['GET'])
# @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def ping():
    response = jsonify('Im active!')
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


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
    redis_key = "{0}-{1}".format(geocodes[0], geocodes[1])
    if redis_instance.hgetall(redis_key):
        data = redis_instance.hgetall(redis_key)
        new_response = {}
        for key, value in data.items():
            str_key = key.decode("utf-8")
            new_response[str_key] = json.loads(value)

        user_location = {"lat": new_response["user_location"][0], "lon": new_response["user_location"][1]}
        current_location = {"lat": lat, "lon": lon}
        distance = controller_utils.miles_between(user_location, current_location)
        if distance < 2.0:
            new_drone = controller_drones.create()
            new_response["drone"]["drone_id"] = new_drone.id_iter
            return jsonify(new_response)

    # response = _cache.get_cache(lat, lon, user_uid)
    # response = _cache.between_two_miles(lat, lon, user_uid)

    if response == {}:
        try:
            controller_api.run(lat, lon, uid)
            args = controller_api.solved_request
            payload = Payload()
            payload.create(args)
            response = payload.parse()
            # store response in redis cache
            new_data = {}
            for key, value in response.items():
                new_data[key] = json.dumps(value)
            redis_instance.hmset(redis_key, new_data)
            # _cache.put_on_cache(response)
        except Exception as response:
            return str(response)

    return jsonify(response)


@app.route('/location-line', methods=['POST'])
def location_gmap_html():
    data = request.get_json()
    user_location = data['user_location']
    school_location = data['school_location']
    redis_key = "location-key {0},{1} - {2},{3}".format(user_location[0], user_location[1], school_location[0], school_location[1])
    if redis_instance.hgetall(redis_key):
        data = redis_instance.hgetall(redis_key)
        return jsonify({"data": data})

    gmap_data = controller_utils.get_gmap_line_html(user_location, school_location)
    response_data = {"data": gmap_data}
    redis_instance.hmset(redis_key, response_data)
    logger.info(response_data)
    return jsonify(response_data)


@app.route('/scrap-street-view-image', methods=['GET'])
def scrap_street_view_image():
    store_image = StoreImage()
    store_image.process_data()
    logger.info("Image store completed")
    return jsonify({"data": "Image store completed"})


@app.route('/smartwatch-data', methods=['POST'])
def handle_smartwatch_data():
    data = request.get_json()
    print(data)
    heart_rate = data['heart_rate']
    location = data['location']
    response = jsonify({"status": True, "heart_rate": heart_rate, "location": location})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response