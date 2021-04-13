import json
import flask
import datetime
from flask import request, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from models import Drone
from controllers import ControllerDrones, ControllerHighSchools, ControllerUsers, ControllerPayload, ControllerAPI, ControllerMongo

from utils import Utils

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# init API
app = flask.Flask(__name__)
# Swagger Doc Specs
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "safeWrd_API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# API configs
config = {
    "DEBUG": True,
    "JSON_SORT_KEYS": False
}
app.config.from_mapping(config)

# Init CORS
cors = CORS(app)

# init controllers objs
controller_utils = Utils()
controller_payload = ControllerPayload()
controller_drones = ControllerDrones()
controlller_schools = ControllerHighSchools()
controller_mongo = ControllerMongo()
controller_users = ControllerUsers()
controller_api = ControllerAPI()

@app.route('/', methods=['GET'])
def ping():
        return jsonify('Im active!')

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

@app.route('/safewrd', methods=['GET'])
def user_location():
    lat, lon, uid = (str(request.args['lat']), str(request.args['lon']), str(request.args['uid']))
    controller_api.run(lat, lon, uid)
    response = controller_payload.create(controller_api.solved_request)
    return jsonify(response.dic())

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000')
