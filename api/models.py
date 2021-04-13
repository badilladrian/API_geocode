import json
import random
import string
from datetime import datetime
import itertools
from json import JSONEncoder
import google_streetview.api
import uuid

class Drone:
    id_iter = itertools.count()
    speed = 0
    def __init__(self):
        self.id_iter = next(Drone.id_iter)
        self.speed = 0

    def update(self, data):
        if data.id:
            self._id = data.id
        if data.speed:
            self.speed = data.speed


class User:
    def __init__(self, username):
        self._uid = _uid
        self._geocode = [0.0,
                        0.0] 

    def update(self, data):
        if data.uid:
            self._uid = data._uid
        if data.geocode:
            self.geocode = data.geocode


class HighSchool:
    def __init__(self, name, address, geocodes):
        self._name = name
        self._address = address
        self._id = uuid.uuid4()
        self._geocodes = geocodes

    def update(self, data):
        if data.name:
            self._name = name
        if data.speed:
          self._address = address

class Payload(object):
    payload = {}
    id_iter = itertools.count()
    
    def __init__(self):
        self.id_iter = next(Payload.id_iter)
        self.payload = {}
        self.args = []
        
    def create(self,args):
        user , geocodes, timestamp, drone, miles, speed, eta_time, school_dict, map_ = args
        self.args = args

        # Download images to directory 'downloads'

        self.payload =   {
                            "user_data": user, 
                            "user_location": geocodes,
                            "date_of_request": str(timestamp), 
                            "payload_id": self.id_iter ,
                            "drone": { 
                                    "drone_id" : drone.id_iter, 
                                    "drone_speed" : speed,
                                    },
                            "miles_distance":  miles, 
                            "estimated_time":  eta_time, 
                            "embedded_map": 'results.links',                
                            "nearest_school":
                                        {
                                        "name": school_dict['name'],
                                        "address": school_dict['address'], 
                                        "geocodes": school_dict['geocodes'],    
                                        "school_image":  school_dict['URL'], 
                                        },
                            "airgeos_vote_url": "https://www.aireos.io/network/"
                    }

    def dic(self):
        iframe2 = """<iframe width="600" height="500" id="gmap_canvas" src="https://maps.google.com/maps?q={}&t=&z=13&ie=UTF8&iwloc=&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>""".format(self.args[7]['URL'])
        iframe = """<!DOCTYPE html><html lang="en"><head>    <meta charset="UTF-8">    <title>IPyWidget export</title></head><body><!-- Load require.js. Delete this if your page already loads require.js --><script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js" integrity="sha256-Ae2Vz/4ePdIu6ZyI/5ZGsYnb+m0JlOmKPjt6XZ9JJkA=" crossorigin="anonymous"></script><script src="https://unpkg.com/@jupyter-widgets/html-manager@^0.20.0/dist/embed-amd.js" crossorigin="anonymous"></script><script type="application/vnd.jupyter.widget-state+json">{  "version_major": 2,  "version_minor": 0,  "state": {    "16cd3775d052470ab7f39fb8060a4b75": {      "model_name": "LayoutModel",      "model_module": "@jupyter-widgets/base",      "model_module_version": "1.2.0",      "state": {        "height": "100%",        "width": "100%"      }    },    "7767345b11c54e19969ad293640a5c97": {      "model_name": "PlainmapModel",      "model_module": "jupyter-gmaps",      "model_module_version": "0.9.0",      "state": {        "_dom_classes": [],        "configuration": {          "api_key": "AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g"        },        "data_bounds": [          [            18.2764112,            -90.79449813119544          ],          [            49.3678704,            -76.61782596880454          ]        ],        "initial_viewport": {          "type": "DATA_BOUNDS"        },        "layers": [          "IPY_MODEL_c3807ab4d8754e3d90b1ffb1b3ac1a2d"        ],        "layout": "IPY_MODEL_16cd3775d052470ab7f39fb8060a4b75"      }    },    "93fa0e2f514b403db129242718a1500e": {      "model_name": "LayoutModel",      "model_module": "@jupyter-widgets/base",      "model_module_version": "1.2.0",      "state": {}    },    "c57f8015368a4cb2be987d8846baacf3": {      "model_name": "ToolbarModel",      "model_module": "jupyter-gmaps",      "model_module_version": "0.9.0",      "state": {        "_dom_classes": [],        "layer_controls": [],        "layout": "IPY_MODEL_93fa0e2f514b403db129242718a1500e"      }    },    "1d5d9dfde6b14bca8e773ba7f93b9203": {      "model_name": "LayoutModel",      "model_module": "@jupyter-widgets/base",      "model_module_version": "1.2.0",      "state": {}    },    "1fc9d89712334d41945e5260e1c09701": {      "model_name": "ErrorsBoxModel",      "model_module": "jupyter-gmaps",      "model_module_version": "0.9.0",      "state": {        "_dom_classes": [],        "errors": [],        "layout": "IPY_MODEL_1d5d9dfde6b14bca8e773ba7f93b9203"      }    },    "724fdb928cf84b5887a3a339ef2f65bb": {      "model_name": "LayoutModel",      "model_module": "@jupyter-widgets/base",      "model_module_version": "1.2.0",      "state": {        "height": "420px"      }    },    "3ac2e68fad284bb3bb913c84fb79dece": {      "model_name": "FigureModel",      "model_module": "jupyter-gmaps",      "model_module_version": "0.9.0",      "state": {        "_dom_classes": [],        "_errors_box": "IPY_MODEL_1fc9d89712334d41945e5260e1c09701",        "_map": "IPY_MODEL_7767345b11c54e19969ad293640a5c97",        "_toolbar": "IPY_MODEL_c57f8015368a4cb2be987d8846baacf3",        "layout": "IPY_MODEL_724fdb928cf84b5887a3a339ef2f65bb"      }    },    "5a21118380714332a73f2a47239d0f55": {      "model_name": "MarkerModel",      "model_module": "jupyter-gmaps",      "model_module_version": "0.9.0",      "state": {        "location": [          26.049276,          -80.163124        ]      }    },    "c4d963b8860345bfb52c4cb7e142d354": {      "model_name": "MarkerModel",      "model_module": "jupyter-gmaps",      "model_module_version": "0.9.0",      "state": {        "location": [          41.5950056,          -87.2492001        ]      }    },    "c3807ab4d8754e3d90b1ffb1b3ac1a2d": {      "model_name": "MarkerLayerModel",      "model_module": "jupyter-gmaps",      "model_module_version": "0.9.0",      "state": {        "data_bounds": [          [            18.2764112,            -90.79449813119544          ],          [            49.3678704,            -76.61782596880454          ]        ],        "markers": [          "IPY_MODEL_5a21118380714332a73f2a47239d0f55",          "IPY_MODEL_c4d963b8860345bfb52c4cb7e142d354"        ]      }    }  }}</script><script type="application/vnd.jupyter.widget-view+json">{"version_major": 2, "version_minor": 0, "model_id": "3ac2e68fad284bb3bb913c84fb79dece"}</script></body></html>"""
        self.payload =   {
                    "user_data": str(self.args[0]), 
                    "user_location": self.args[1],
                    "date_of_request": str(self.args[2]), 
                    "payload_id": self.id_iter ,
                    "drone": { 
                            "drone_id" : self.args[3].id_iter, 
                            "drone_speed" :  self.args[6],
                            },
                    "miles_distance":  self.args[4], 
                    "estimated_time":  self.args[5], 
                    "embedded_map": iframe2,    
                    "nearest_school":
                                {
                                "name": self.args[7]['name'],
                                "address": self.args[7]['address'], 
                                "geocodes": self.args[7]['geocodes'],    
                                "school_image":  "https://maps.googleapis.com/maps/api/streetview?size=600x300&location={}&key=AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g".format(self.args[7]['URL']), 
                                },
                    "aireos_vote_url": "https://www.aireos.io/network/"
            }      
        return self.payload

    def generate_id(self, id_ctr):
        caracters = string.ascii_letters + string.digits 
        add_unique_value = ''.join(random.choice(caracters) for i in range(8))
        return '{}_safewrd_{}'.format(id_ctr, add_unique_value)
