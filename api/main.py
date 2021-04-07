import flask
import datetime
from flask import request, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from models import Drone
from controllers import ControllerDrones

from utils import Utils

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)

### swagger specific ###
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
### end swagger specific ###


controller_utils = Utils()
controller_drones = ControllerDrones()
controller_drones.create(345)
drone =  Drone(345)

@app.route('/', methods=['GET'])
def ping():
        return jsonify('Im active!')

@app.route('/safewrd', methods=['GET']) #GFM
def user_location():
    lat, lon = [0.0,0.0]
    #lat, lon = [10.007580834414526, -84.14959156949683]
    if 'lat' in request.args:
        lat = (request.args['lat'])

    if 'lon' in request.args:
        lon = (request.args['lon'])

    user_location = [str(lat), str(lon)]

    closest_hs_geocodes = controller_utils.find_closest_lat_lon(controller_utils._school_list,
                                                    {'lat':float(lat),'lon':float(lon)} )

    miles_from_user_to_school = controller_utils.miles_between(user_location, [str(closest_hs_geocodes['lat']),
                                                              str(closest_hs_geocodes['lon']) ])
                

    time = (miles_from_user_to_school/80) * 60
    
    myDrone = controller_drones.get(345)
    
    result = {
        #"drone_id": drone._id,
        
        "drone_id": myDrone._id,
        "drone_speed": myDrone._speed,
        "miles_user_to_school": str(miles_from_user_to_school) + ' miles',
        "estimated_time": str(time) + ' min',
        "nearest_school":
            {
                "address": controller_utils.geocode_to_address(closest_hs_geocodes), 
                "geocodes": closest_hs_geocodes,     
                "image": 'im_an_image'
            }
        }

    return jsonify(result)

app.run()