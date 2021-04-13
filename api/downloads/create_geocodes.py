import csv
import pandas as pd
import googlemaps

def add_geoodes(start, stop, images_id, batch):
    gmaps = googlemaps.Client(key='AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g')
    df = pd.read_csv("HS_data_no_repeated.csv")
    geocodes=[]
    addresses=[]
    names=[]
    index = start
    images_processed = images_id
    while index < stop:
        address = df.iloc[index]['Address']
        name = df.iloc[index]['Company']
        geocode_from_school = gmaps.geocode(address) 
        if geocode_from_school:    
            geocodes.append(geocode_from_school[0]["geometry"]['location'])
            addresses.append(geocode_from_school[0]["formatted_address"])
            names.append(name)
            images_processed = images_processed + 1
            print(images_processed)
        index = index + 1

    new_school_data = pd.DataFrame(
    {'Name': names,
    'Address': addresses,
    'Geocodes': geocodes
    })
        
    new_school_data.to_csv("HS_ADR_GS_{}.csv".format(batch))
    return images_processed

ids_track = add_geoodes(2700,3000,2700,'K') 
ids_track = add_geoodes(3000,3300,3000,'I') 
ids_track = add_geoodes(3300,3700,3300,'M') 
ids_track = add_geoodes(3700,4100,3700,'N') 
