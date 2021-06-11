import os, sys
import requests
import json
import gmaps
import requests
import googlemaps
from geopy.distance import geodesic
from ipywidgets.embed import embed_minimal_html
from math import radians, cos, sin, asin, sqrt, inf
from api import BASE_DIR
from bs4 import BeautifulSoup


class Utils:
    def __init__(self):
        self.api_key = 'AIzaSyDyn3nhSkxdxS6aUJXim4O-T50ZtLg4YGY'
        gmaps.configure(api_key=self.api_key)
        self.google_client = googlemaps.Client(key=self.api_key)

    def dist(self, lat1, long1, lat2, long2):
        """
    Replicating the same formula as mentioned in Wiki
        """
        # convert decimal degrees to radians 
        lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
        # haversine formula 
        dlon = long2 - long1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        # Radius of earth in kilometers is 6371
        km = 6371 * c
        return km

    def get_closest(self, user, schools):
        last_dist = inf
        for item in schools:
            dist_between = self.dist(user[0], user[1], item['lat'], item['lon'])
            if dist_between < last_dist:
                closest_school = item
                last_dist = dist_between
            else:
                last_dist = dist_between
        return closest_school

    # calculate the Euclidean distance between two vectors
    def euclidean_distance(self, row1, row2):
        distance = 0.0
        for i in range(len(row1) - 1):
            distance += (row1[i] - row2[i]) ** 2
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
        school_geocode = (float(school_geocode['lat']), float(school_geocode['lon']))
        user_location = (float(user_location['lat']), float(user_location['lon']))
        miles = geodesic(user_location, school_geocode).miles
        return miles

    def address_to_geocode(self, address):
        """ GOOGLE API from address to geocodes"""
        geocode_result = self.google_client.geocode(address)
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lon = geocode_result[0]["geometry"]["location"]["lng"]
        return (lat, lon)

    def google_map_markers(self, user_location, school_geocodes):
        """ Gmaps to create HTML map with two markers geolocations"""
        embedded_map = gmaps.figure()
        user_geocode = (float(user_location[0]), float(user_location[1]))
        school_geocodes = (float(school_geocodes['lat']), float(school_geocodes['lon']))
        markers = [user_geocode, school_geocodes]
        custom_marker = gmaps.marker_layer(markers)
        embedded_map.add_layer(custom_marker)
        return embedded_map
        # embed_minimal_html('export.html', views=[embedded_map])

    def address_from_geocode(self, geocode):
        base = "https://maps.googleapis.com/maps/api/geocode/json?"
        params = "latlng={},{}&sensor=True&key={}".format(geocode[0], geocode[1],
                                                          self.api_key)
        url = "{}{}".format(base, params)
        response = requests.get(url)
        response = response.json()
        address = response['results'][0]['formatted_address']
        return address

    def get_gmap_line_html(self, user_location, school_location):
        file_path = "{0}/gmap_line.html".format(BASE_DIR)
        _file_data = self._open_file(file_path)
        soup = BeautifulSoup(_file_data, 'html.parser')
        map_div = soup.select_one("#map")
        map_header_style = soup.select_one("style")
        header_script_tag = soup.new_tag("script")
        bootom_script_tag = soup.new_tag("script")
        gmap_script = "https://maps.googleapis.com/maps/api/js?key={0}&callback=initMap&libraries=&v=weekly".format(
            self.api_key)
        bootom_script_tag['src'] = gmap_script
        center_lat = user_location[0] - 0.00200
        center_long = user_location[1] + 0.00300
        header_script = '''
            function initMap() {
                const myLatLng = { lat: ''' + "{:.5f}".format(center_lat) + ''', lng: '''+ "{:.5f}".format(center_long) +''' }
                const map = new google.maps.Map(document.getElementById("map"), {
                  zoom: 3,
                  center: myLatLng,
                  mapTypeId: "terrain",
                });
                const flightPlanCoordinates = [
                  { lat: ''' + str(user_location[0]) + ''', lng: ''' + str(
            user_location[1]) + ''' },
                  { lat: ''' + str(school_location[0]) + ''', lng: ''' + str(
            school_location[1]) + ''' }
                ];
                const flightPath = new google.maps.Polyline({
                  path: flightPlanCoordinates,
                  geodesic: true,
                  strokeColor: "#FF0000",
                  strokeOpacity: 1.0,
                  strokeWeight: 2,
                });
                flightPath.setMap(map);
              }
        '''
        header_script_tag.append(header_script)
        map_div.insert_after(bootom_script_tag)
        map_header_style.insert_after(header_script_tag)
        return soup.prettify()

    def _open_file(self, file_path):
        with open(file_path, 'r') as f:
            data = f.read()
            f.close()
            return data

    def distance_of_two_points(self, point1, point2):
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "units": "imperial",
            "origins": "{0},{1}".format(point1[0], point1[1]),
            "destinations": "{0},{1}".format(point2[0], point2[1]),
            "key": self.api_key
        }
        response = requests.get(url, params=params)
        return response.json(), response.status_code
