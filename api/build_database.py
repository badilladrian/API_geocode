from pymongo import MongoClient
import os
import csv
import pandas as pd
import googlemaps
from bson.objectid import ObjectId
from api.models import HighSchool
import pprint


class MongoDB:
    def __init__(self, max_pool_size=50):
        self._client = MongoClient(['104.236.59.158'], 27017, maxPoolSize=max_pool_size)
        self._database = self._client['geocodes_api']
        self._collection = self._database['schools']

    def create(self, school):
        if school is not None:
            self._collection.insert(school)            
        else:
            raise Exception("Nothing to save, because school parameter is None")

    def load_data_to_mongo(self, full_path_file):
        with open(full_path_file, "r", encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            csv_reader_list = list(csv_reader)
            for value in range(0, len(csv_reader_list)):
                self._collection.insert_many(csv_reader_list[value:value], ordered=False)
            csv_file.close()

    def read(self, school_id=None):
        if school_id is None:
            return self._db.geocode.school.find({})
        else:
            cursor = self._db.geocode.school.find_one({"_id":'"606fd0b9ff4969c6e6e871fd"'})
            return cursor

    def update(self, school):
        if school is not None:
            # the save() method updates the document if this has an _id property 
            # which appears in the collection, otherwise it saves the data
            # as a new document in the collection
            self.geocode.schools.save(school.get_as_json())            
        else:
            raise Exception("Nothing to update, because school parameter is None")


    def delete(self, school):
        if school is not None:
            self.geocode.school.remove(school.get_as_json())            
        else:
            raise Exception("Nothing to delete, because school parameter is None")


    def load_data_to_mongo1(self):
        self._collection.insert_many(self.csv_to_json())

    def csv_to_json(self):
        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))        
        data = pd.read_csv(str(__location__) +'/HS_ADR_GS_A.csv',usecols= ['name','address', 'geocodes'])
        return data.to_dict()

    # def add_geoodes(self):
    #     df = pd.read_csv("HS_data_no_repeated.csv")
    #     geocodes=[]
    #     index = 0
    #     while index < int(df.size-1):
    #         address = df.iloc[index]['Address']
    #         geocode_from_school = self.gmaps.geocode(address) 
    #         if geocode_from_school:    
    #             geocodes= geocode_from_school[0]["geometry"]['location']
    #         index = index + 1
    #     df['Geocodes'] = pd.geocodes(geocodes)
    #     df.to_csv(index=False)
                



if __name__ == '__main__':

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    mongodb = MongoDB()
    print("Saving data in the database.... ")

    # mongodb.load_school_df()
    mongodb.load_data_to_mongo()

    print("Process finished...")