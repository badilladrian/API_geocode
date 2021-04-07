from re import S
import googlemaps
from datetime import datetime

from geopy.distance import geodesic

class Utils:
    def __init__(self):
        school_0 = {'lat':10.007580834414526, 'lon': -84.14959156949683}
        school_1 = {'lat': 40.712776, 'lon': -74.005974}
        school_2 = {'lat': 47.751076,  'lon': -120.740135}
        school_3 = {'lat': 37.774929, 'lon': -122.419418}  
        
        self._school_list = [school_0,school_1, school_2, school_3]
        self._google_api = googlemaps.Client(key='AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g')

    def dist_between_two_lat_lon(self, *args):
        from math import asin, cos, radians, sin, sqrt
        lat1, lat2, long1, long2 = map(radians, args)

        dist_lats = abs(lat2 - lat1) 
        dist_longs = abs(long2 - long1) 
        a = sin(dist_lats/2)**2 + cos(lat1) * cos(lat2) * sin(dist_longs/2)**2
        c = asin(sqrt(a)) * 2
        radiusEarth = 6378 # the "Earth radius" R varies from 6356.752 km at the poles to 6378.137 km at the equator.
        return c * radiusEarth

    def find_closest_lat_lon(self, data, userLocation):
        try:
            geoCodes = min(data, key=lambda p: self.dist_between_two_lat_lon(userLocation['lat'],
                                                        userLocation['lon'],p['lat'],p['lon']))
            return geoCodes
        except TypeError:
            print('Not a list or not a number.')

    def geocode_to_address(self, geoCode):
        response = self._google_api.reverse_geocode((geoCode['lat'], 
                                                geoCode['lon']))
        flatAddress = response[2]['formatted_address']
        return flatAddress

    def address_to_geocode(self, address):
        if address: #GFM
            return self._google_api.geocode(address) #GFM
        else: #GFM
            return self._google_api.geocode('1600 Amphitheatre Parkway, Mountain View, CA')        

    def miles_between(self, userLocation, schoolGeocode):
        miles = geodesic(userLocation,schoolGeocode).miles
        return miles