import logging
import datetime
import os
import json
import pandas as pd
from utils import Utils

class ControllerCache:
    def __init__(self):
        self._cache_responses = []
        self.load_cache()

    def get_cache(self, lat, lon):
        found_answer = [ payload for payload in self._cache_responses if payload['user_location'] == [lat, lon]] # if same geocodes
        if found_answer:
            return found_answer
        else:
            cache_data = [ [payload['user_location'], payload['payload_id'], payload['drone']['drone_id']] for payload in self._cache_responses]
            geocode = [lat, lon]             # if request between 2miles ratios
            for record in cache_data:
                miles_between = float(Utils.miles_between(geocode, record[0]))
                if miles_between <= 2.0:
                    found_answer = record['payload_id']
                    break
            found_answer = [ payload for payload in self._cache_responses if payload['payload_id'] == found_answer]
            return found_answer[0]
        return False            
        
    def put_on_cache(self, response_payload):
        dict_payload = response_payload.dic()
        with open('cache.json', 'w') as json_file:
            if len(json_file.readlines())<1:
                json_file.write('[')
                json_file.write(']')
        with open('cache_read.json', 'w') as modified: 
            modified.write("\n" + data + "\n" )     
            modified.write("]")              
            json.dump(dict_payload, json_file)

    def load_cache(self):
        try:
            # lines = []
            # data = {}
            # with open('cache.json') as file_:
            #     lines = file_.readlines()
            # if lines:
            #     with open('cache.json', 'r') as original: 
            #         data = original.read()
            #     with open('cache_read.json', 'w') as modified: 
            #         modified.write("[" + data)     
            #         modified.write("]")          
            #     with open('cache_read.json') as json_file:
            #         data = json.load(json_file)
            
            self._cache_responses = payloads
        except:
            self._cache_responses = False
