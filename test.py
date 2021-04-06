#!/usr/bin/env python3
import yaml

credentials = yaml.load(open('./gmaps.yaml'))
url = credentials['database']['url']
api_key = credentials['database']['GOOGLE_API_KEY']
print("URL: " +url)
print("Key: " +api_key)