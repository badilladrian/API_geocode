import csv
import pandas as pd
import googlemaps

def add_geoodes(start, stop, images_id, batch):
    gmaps = googlemaps.Client(key='AIzaSyDyn3nhSkxdxS6aUJXim4O-T50ZtLg4YGY')
    df = pd.read_csv("schools.csv")
    geocodes=[]
    addresses=[]
    names=[]
    index = start
    images_processed = images_id
    while index < stop:
        name = df.iloc[index]['NAME']
        full_address = df.iloc[index]['FullAddress']
        website = df.iloc[index]['WEBSITE']
        geocode_from_school = gmaps.geocode(full_address) 
        if geocode_from_school:
            geocodes.append(geocode_from_school[0]["geometry"]['location'])
            addresses.append(geocode_from_school[0]["formatted_address"])
            names.append(name)
            print(geocode_from_school[0]["formatted_address"], images_processed)
            images_processed = images_processed + 1
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

ids_track = add_geoodes(16700,17000,16700,'12') 
