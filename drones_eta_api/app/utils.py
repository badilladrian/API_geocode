import googlemaps
import google_streetview.api
from datetime import datetime
from math import cos, asin, sqrt
from geopy.distance import geodesic



class Utils:
    def __init__(self):
        self._google_api = googlemaps.Client(key='AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g')

    def distance(self,*args):
        p = 0.017453292519943295
        a = 0.5 - cos((args[2]-args[0])*p)/2 + cos(args[0]*p)*cos(args[2]*p) * (1-cos((args[3]-args[2])*p)) / 2
        return 12742 * asin(sqrt(a))

    def closest(self,data, v):
        return min(data, key=lambda p: self.distance(v['lat'],v['lon'],p['lat'],p['lon']))

    def time_stamp(self):
        return datetime.now()

    def geocode_to_address(self, geocode):
        response = self._google_api.reverse_geocode((geocode['lat'], 
                                                geocode['lon']))
        flat_address = response[2]['formatted_address']
        return flat_address

    def address_to_geocode(self, address):
        return self._google_api.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

    def miles_between(self, user_location, school_geocode):
        miles = geodesic(user_location,school_geocode).miles
        return miles

    def google_map_markers(self, user_location, drone_location):
        embedded_map = gmaps.figure(center=(51.5, 0.1), zoom_level=9)
        
        markers=[(user_location),(drone_location)]


        custom_marker = self._google_api.symbol_layer(
            markers, fill_color='green', stroke_color='blue')

        embedded_map = self._google_api.add_layer(custom_marker)

        return embedded_map  

    def google_draw_line(self, embedded_map, geocodes):
        straigth_line = self._google_api.Line(
            start=(geocodes.pop()),
            end=(geocodes.pop()),
            stroke_weight=3.5
        )
        drawing = self._google_api.drawing_layer(features=[straigth_line])
        embedded_map.add_layer(drawing)

    def add_to_iFrame(self, view_type, gecodes):
        html = '<iframe \
                    width="450"\
                    height="250"\
                    frameborder="0" style="border:0"\
                    src="https://www.google.com/maps/embed/v1/view_type?key=AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g \
                    &center= geocodes \
                    &zoom=18 \
                    &maptype=satellite" allowfullscreen> \
                </iframe>'.replace('gecodes', gecodes)
        html = html.replace('view_type', view_type)

        return html

    def street_view_school(self, geocodes):
        params = [{
            'size': '600x300', # max 640x640 pixels
            'location': geocodes,
            'heading': '151.78',
            'pitch': '-0.76',
            'key': 'AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g'
            }]
        results = google_streetview.api.results(params)
        results.save_links('links.txt')
        results.save_metadata('metadata.json')
        return results