import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key="AIzaSyC9_hj9Dx9xRtLls8JXDTO82MY6Pf0FNfI")

geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')


                # Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((22.5757344, 88.4048656))


print(reverse_geocode_result)