import requests, json
  
api_key ="AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g"

#source = "'lat': 39.7612992, 'lon': -86.1519681"  
source = "39.7612992, -86.1519681"
  
#dest = "'lat': 39.7622292, 'lon': -86.1578917"
dest = "39.7622292,-86.1578917"
  
url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
  
# return response object
result = requests.get(url + 'origins=' + source +
                   '&destinations=' + dest +
                   '&key=' + api_key)
                     
# return json format result
eta_time = result.json()
ETA = eta_time['rows'][0]['elements'][0]['duration']['text']    
print(ETA)