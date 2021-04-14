# API_geocode
use pipenv shell
pipenv install -r requirements.txt
then: python main.py

# REQUEST
POST /safewrd
``` 

        {
        "geocodes": [38.8254326, -97.7021551],
        "uid": "CA308008-421B-11EB-B2BF-EDEFCE1D72FE"
        }
``` 


# RESPONSE
``` 
{
    "user_data": "CA308008-421B-11EB-B2BF-EDEFCE1D72FE",
    "user_location": [
        38.8254326,
        -97.7021551
    ],
    "date_of_request": "2021-04-14 02:43:30.720715",
    "payload_id": "0_safewrd_wTkX1FqA",
    "drone": {
        "drone_id": 0,
        "drone_speed": "2395.59 ml/h"
    },
    "miles_distance": "3194.12 miles",
    "estimated_time": "1.33 minutes",
    "embedded_map": "<iframe width=\"600\" height=\"500\" id=\"gmap_canvas\" src=\"https://maps.google.com/maps?q=Diomede%2C%20AK%2099762%2C%20USA&t=&z=13&ie=UTF8&iwloc=&output=embed\" frameborder=\"0\" scrolling=\"no\" marginheight=\"0\" marginwidth=\"0\"></iframe>",
    "nearest_school": {
        "name": "MORGAN ENTERPRISES",
        "address": "Diomede, AK 99762, USA",
        "geocodes": {
            "lat": 64.50114429999999,
            "lon": -165.4064968
        },
        "school_image": "https://maps.googleapis.com/maps/api/streetview?size=600x300&location=Diomede%2C%20AK%2099762%2C%20USA&key="
    },
    "aireos_vote_url": "https://www.aireos.io/network/"
}
``` 

# API Summary:
-> controllers do all the interactions
-> models only define objects (payload creates the API respond!) * maps 
-> street viewer can download school images
-> utils has all the necessary functions for the application

# cache LOGIC
-> the same response is returned if the same geocode makes a query
-> the same response is returned if new request is inside ratio of 2miles of previous requests
-> we must eventually save the images and stop consulting google for everytime * 

# chart-values 
-> API key (not actually being used now)

# static 
-> contains the iFrame that I placed but we need to pass the HTML gmaps w/ markers
-> contains the metadata needed to get header of pic to get actual picture from street_view.py Task4
-> other jsons for reference. There is a payload response as well --- 


# TASKS: I commented all the code- feel free to delete comments as needed. Did my best
-> you can look for the notes in the project they are TASK#--N 
TASK#--1 How to deploy at server properly using SSL+HTTPS+UWSGI+NGIX
TASK#--2 How to pass a whole HTML in the response
TASK#--3 Save image from google and then re-use it when needed
TASK#--4 Cache 
TASK#--5 OpenAPI
TASK#--6 Sentry