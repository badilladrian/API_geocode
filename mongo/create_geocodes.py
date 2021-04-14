import csv
import pandas as pd
import googlemaps

def add_geoodes(start, stop, images_id, batch):
    gmaps = googlemaps.Client(key='AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g')
    df = pd.read_csv("HS_data.csv")
    geocodes=[]
    addresses=[]
    names=[]
    index = start
    images_processed = images_id
    while index < stop:
        address = df.iloc[index]['Address']
        county = df.iloc[index]['County']
        state = df.iloc[index]['State']
        zip_ =df.iloc[index]['Zip']
        name = df.iloc[index]['Company']
        full_address = address+' '+county+' '+state+' '+zip_ + 'US'
        geocode_from_school = gmaps.geocode(full_address) 
        if geocode_from_school:    
            geocodes.append(geocode_from_school[0]["geometry"]['location'])
            addresses.append(geocode_from_school[0]["formatted_address"])
            names.append(name)
            images_processed = images_processed + 1
            print(full_address, geocode_from_school[0]["formatted_address"])
            print(images_processed)
        index = index + 1

    new_school_data = pd.DataFrame(
    {
    '_id': range(start, images_processed),
    'Name': names,
    'Address': addresses,
    'Geocodes': geocodes
    })
        
    new_school_data.to_csv("HS_ADR_GS_{}.csv".format(batch))
    return images_processed

ids_track = add_geoodes(0,1000,0,'A') 
ids_track = add_geoodes(1000,2000,1000,'B') 
ids_track = add_geoodes(2000,3000,2000,'C') 
ids_track = add_geoodes(3000,4000,3000,'D') 
