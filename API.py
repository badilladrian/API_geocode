import requests, json
from datetime import datetime
api_key ='AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g'
url ='https://maps.googleapis.com/maps/api/distancematrix/json?'


#Functions
def dist_between_two_lat_lon(*args):
    from math import asin, cos, radians, sin, sqrt
    lat1, lat2, long1, long2 = map(radians, args)

    dist_lats = abs(lat2 - lat1) 
    dist_longs = abs(long2 - long1) 
    a = sin(dist_lats/2)**2 + cos(lat1) * cos(lat2) * sin(dist_longs/2)**2
    c = asin(sqrt(a)) * 2
    radius_earth = 6378 # the "Earth radius" R varies from 6356.752 km at the poles to 6378.137 km at the equator.
    return c * radius_earth

def find_closest_lat_lon(data, v):
    try:
        return min(data, key=lambda p: dist_between_two_lat_lon(v['lat'],v['lon'],p['lat'],p['lon']))
    except TypeError:
        print('Not a list or not a number.')

#GET info from APP server and DB

school_1 = {'lat': 40.712776, 'lon': -74.005974}
school_2 = {'lat': 47.751076,  'lon': -120.740135}
school_3 = {'lat': 37.774929, 'lon': -122.419418}

city_list = [school_1, school_2, school_3]

user_location = {'lat': 25.806206, 'lon': -80.263124 } #lat,lon
usr_lat = str(user_location['lat']) 
usr_lon = str(user_location['lon'])
dest = usr_lat + ',' + usr_lon


source = find_closest_lat_lon(city_list, user_location)
or_lat = str(source['lat'])
or_lon = str(source['lon'])
origin = or_lat + ',' + or_lon
print(origin)


result = requests.get(url + 'origins=' + origin +
                   '&destinations=' + dest +
                   '&key=' + api_key)

# return json format result
closer_drone = json.dumps(source)
eta_time = result.json()
ETA = json.dumps(eta_time['rows'][0]['elements'][0]['duration']['text'])    

#Send result as json
print("Closer Drone geocode =" +closer_drone)
print("ETA =" +ETA)