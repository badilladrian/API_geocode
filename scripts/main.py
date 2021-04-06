import requests
import googlemaps
from datetime import datetime

coords_0 = '43.70721,-79.3955999' # one place
coords_1 = '43.7077599,-79.39294' # another place

gmaps = googlemaps.Client(key="AIzaSyC9_hj9Dx9xRtLls8JXDTO82MY6Pf0FNfI")

now = datetime.now()

            # Directions API
response = gmaps.directions(coords_0, coords_1, mode="driving", departure_time=now, avoid='tolls')

print(response)

# total distance straigth line * drones to whatever needed speed per hour
# always under 2 > minutes

# display google maps with the pin on the nearest HS

distance = 0 
legs = response[0].get("legs")

for leg in legs:
    distance = distance + leg.get("distance").get("value")

print(distance) 
