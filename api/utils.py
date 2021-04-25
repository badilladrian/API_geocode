import os, sys
import requests
import gmaps
import googlemaps
from math import cos, asin, sqrt
from geopy.distance import geodesic
from ipywidgets.embed import embed_minimal_html

class Utils:
    def __init__(self):
        self.api_key = 'AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g'
        gmaps.configure(api_key=self.api_key) 
        self.google_client = googlemaps.Client(key=self.api_key)

    def distance(self,*args):
        """ Calculates closest geolocation from user to a list of options"""
        p = 0.017453292519943295
        a = 0.5 - cos((args[2]-args[0])*p)/2 + cos(args[0]*p)*cos(args[2]*p) * (1-cos((args[3]-args[2])*p)) / 2
        return 12742 * asin(sqrt(a))

    def closest(self,data, v): 
        """ This is the Haversine Formula"""
        return min(data, key=lambda p: self.distance(v['lat'],v['lon'],p['lat'],p['lon']))

    def miles_between(self, user_location, school_geocode):
        """ Calculates miles between two geolocations"""
        school_geocode = (float(school_geocode[0]), float(school_geocode[1]))
        user_location = (float(user_location['lat']), float(user_location['lon']))
        miles = geodesic(user_location,school_geocode).miles
        return miles

    def address_to_geocode(self,address):    
        """ GOOGLE API from address to geocodes"""    
        geocode_result = self.google_client.geocode(address)
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lon = geocode_result[0]["geometry"]["location"]["lng"]
        return (lat,lon)

    def google_map_markers(self, user_location, school_geocodes):
        """ Gmaps to create HTML map with two markers geolocations"""
        embedded_map = gmaps.figure()
        user_geocode = (float(user_location[0]),float(user_location[1]))
        school_geocodes = (float(school_geocodes['lat']),float(school_geocodes['lon']))
        markers=[user_geocode,school_geocodes]
        custom_marker = gmaps.marker_layer(markers)         
        embedded_map.add_layer(custom_marker)
        # embed_minimal_html('export.html', views=[embedded_map])


