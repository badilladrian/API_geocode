import os, sys
import requests
import gmaps
import googlemaps
from math import cos, asin, sqrt
from geopy.distance import geodesic
from ipywidgets.embed import embed_minimal_html

class Utils:
    def __init__(self):
        self.api_key = 'AIzaSyDyn3nhSkxdxS6aUJXim4O-T50ZtLg4YGY'
        gmaps.configure(api_key=self.api_key) 
        self.google_client = googlemaps.Client(key=self.api_key)

    def dist_between_two_lat_lon(self, *args):
        """ Calculates closest geolocation from user to a list of options"""

        from math import asin, cos, radians, sin, sqrt
        lat1, lat2, long1, long2 = map(radians, args)

        dist_lats = abs(lat2 - lat1) 
        dist_longs = abs(long2 - long1) 
        a = sin(dist_lats/2)**2 + cos(lat1) * cos(lat2) * sin(dist_longs/2)**2
        c = asin(sqrt(a)) * 2
        radius_earth = 6378
        return c * radius_earth

    def find_closest_lat_lon(self, data, user_location):
        """ This is the Haversine Formula"""
        try:
            return min(data, key=lambda p: self.dist_between_two_lat_lon(user_location['lat'],
                                                        user_location['lon'],p['lat'],p['lon']))
        except TypeError:
            print('Not a list or not a number.') 

    # calculate the Euclidean distance between two vectors
    def euclidean_distance(self, row1, row2):
        distance = 0.0
        for i in range(len(row1)-1):
            distance += (row1[i] - row2[i])**2
        return sqrt(distance)
    
    # Locate the most similar neighbors
    def get_neighbors(self, train, user_location, num_neighbors=14500):
        distances = list()
        for train_row in train:
            dist = self.euclidean_distance(user_location, train_row)
            distances.append((train_row, dist))
        distances.sort(key=lambda tup: tup[1])
        neighbors = list()
        for i in range(num_neighbors):
            neighbors.append(distances[i][0])
        return neighbors[0]

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


