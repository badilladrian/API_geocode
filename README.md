# API_geocode
use pipenv shell
pipenv install -r requirements.txt
then: python main.py

# REQUEST
POST /safewrd
``` 

        {
        "geocodes": [38.8254326, -97.7021551],
        "uid": CA308008-421B-11EB-B2BF-EDEFCE1D72FE
        }
``` 


# RESPONSE


# downloads contiene los csvs (miguel los va a remplazar)
-> scripts para crear de CSVs a Mongo, y para agregarle a un CSV su geocodes segun el address

# en API tenemos toda la aplicacion
-> controllers do all the interactions
-> models only define objects (payload creates the API respond!) * maps 
-> street viewer can download school images
-> utils has all the necessary functions for the application
# cache 
-> the same response is returned if the same geocode makes a query
-> the same response is returned if new request is inside ratio of 2miles of previous requests
-> we must eventually save the images and stop consulting google for each one

# chart-values 
-> API key (not actually being used now)

# static contains the iFrame + the HTML gmaps w/ markers + the metadata & header of picture and the PICTURE from STREET_VIEW.PY
-> files only for reference. There is a payload response as well



