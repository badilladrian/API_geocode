# import requests
# import googlemaps
# from datetime import datetime

# coords_0 = '43.70721,-79.3955999' # one place
# coords_1 = '43.7077599,-79.39294' # another place

# gmaps = googlemaps.Client(key="AIzaSyC9_hj9Dx9xRtLls8JXDTO82MY6Pf0FNfI")

# now = datetime.now()

#             # Directions API
# response = gmaps.directions(coords_0, coords_1, mode="driving", departure_time=now, avoid='tolls')

# print(response)

# # total distance straigth line * drones to whatever needed speed per hour
# # always under 2 > minutes

# # display google maps with the pin on the nearest HS

# distance = 0 
# legs = response[0].get("legs")

# for leg in legs:
#     distance = distance + leg.get("distance").get("value")

# print(distance) 

import flask
from flask import request, jsonify
from flask_cors import CORS

from utils import Utils

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)

controller_utils = Utils()

@app.route('/', methods=['GET'])
def ping():
        return jsonify('Im active!')

@app.route('/safewrd-api', methods=['GET'])
def user_location():
    lat, lon = [0.0,0.0]

    if 'lat' in request.args:
        lat = (request.args['lat'])

    if 'lon' in request.args:
        lon = (request.args['lon'])

    result = controller_utils.find_closest_lat_lon(controller_utils._school_list,
                                                    {'lat':float(lat),'lon':float(lon)} )

    return jsonify(result)

app.run()