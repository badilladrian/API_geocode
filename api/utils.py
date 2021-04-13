from datetime import datetime
from math import cos, asin, sqrt
from geopy.distance import geodesic
import requests
from matplotlib.pyplot import figure
import matplotlib
import mpld3
from street_viewer import StreetViewer
import gmaps
from ipywidgets.embed import embed_minimal_html
import googlemaps



class Utils:
    def __init__(self):
        self.meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
        self.pic_base = 'https://maps.googleapis.com/maps/api/streetview?'
        self.api_key = 'AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g'
        gmaps.configure(api_key=self.api_key)
        self.google_client = googlemaps.Client(key=self.api_key)


        # define the params for the picture request
        self.pic_params = {'key': self.api_key,
                    'location': 'location',
                    'size': "640x640"}

    def getMetada(self, location):
        self.meta_params = {'key': self.api_key,
                    'location': location}
        meta_response = requests.get(meta_base, params=meta_params)
        return meta_response.json()

    def getPictures(self, location):
        pic_response = requests.get(pic_base, params=pic_params)
        pictures = {"key": '', "value":''}
        for key, value in pic_response.headers.items():
           (f"{key}: {value}")
        return pictures, pictures.ok

    def saveImages(self):
        image_id =  "001"
        with open('image'+image_id+'.jpg', 'wb') as file:
            file.write(pic_response.content)
        pic_response.close()
        return pic_response.content

    def getImage(self):
        plt.figure(figsize=(10, 10))
        img=mpimg.imread('test.jpg')
        imgplot = plt.imshow(img)
        plt.show()
        # or
        # ax = fig.gca()
        # ax.plot([1,2,3,4])

        # mpld3.show(fig)        

    def request_image(self,location):
        gwu_viewer = StreetViewer(api_key=self.api_key,
                            location=location)
        gwu_viewer.get_meta()
        gwu_viewer.get_pic()

    def distance(self,*args):
        p = 0.017453292519943295
        a = 0.5 - cos((args[2]-args[0])*p)/2 + cos(args[0]*p)*cos(args[2]*p) * (1-cos((args[3]-args[2])*p)) / 2
        return 12742 * asin(sqrt(a))

    def closest(self,data, v):
        return min(data, key=lambda p: self.distance(v['lat'],v['lon'],p['lat'],p['lon']))

    def time_stamp(self):
        return datetime.now()

    def miles_between(self, user_location, school_geocode):
        school_geocode = (float(school_geocode[0]), float(school_geocode[1]))
        user_location = (float(user_location['lat']), float(user_location['lon']))
        miles = geodesic(user_location,school_geocode).miles
        return miles

    def address_to_geocode(self,address):        
        geocode_result = self.google_client.geocode(address)
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lon = geocode_result[0]["geometry"]["location"]["lng"]
        return (lat,lon)

    def google_map_markers(self, user_location, school_geocodes):
        embedded_map = gmaps.figure()
        user_geocode = (float(user_location[0]),float(user_location[1]))
        school_geocodes = (float(school_geocodes[0]),float(school_geocodes[1]))
        markers=[user_geocode,school_geocodes]
        custom_marker = gmaps.marker_layer(markers)
        embedded_map.add_layer(custom_marker)
        embed_minimal_html('export.html', views=[embedded_map])

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
        results.save_metadata('metadata.json')
        return results


