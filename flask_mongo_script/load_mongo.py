from pymongo import MongoClient
import os
import csv


class MongoDB:
    def __init__(self, db_name, collection_name, host, port, file_path, inserting_batch, max_pool_size=50):
        self._db_name = db_name
        self._collection_name = collection_name
        self._client = MongoClient(host, port, maxPoolSize=max_pool_size)
        self._data = self._client.large_data.data
        self._file_path = file_path
        self._DB = self._client[self._db_name]
        self._collection = self._DB[self._collection_name]
        self._inserting_batch = inserting_batch

    def load_data_to_mongo(self, full_path_file):
        with open(full_path_file, "r", encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            csv_reader_list = list(csv_reader)
            for value in range(0, len(csv_reader_list), self._inserting_batch):
                self._collection.insert_many(csv_reader_list[value:value + self._inserting_batch], ordered=False)
            csv_file.close()


if __name__ == '__main__':
    print("Mongo DB Process started")
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    settings = {
        'host': '104.236.59.158',
        'port': 27017,
        'file_path': str(__location__) + '/',
        'inserting_batch': 100,
        'db_name': 'geocodes_api',
        'collection_name': 'schools'
    }
    mongodb = MongoDB(**settings)
    print("Dropping Mongo DB ...")
    mongodb._collection.drop()
    print("Dropped Mongo DB ...")

    print("Saving data in the database.... ")

    files_list = os.listdir(mongodb._file_path)
    for file in files_list:
        if file.endswith('.csv'):
            full_path_file = mongodb._file_path + file
            mongodb.load_data_to_mongo(full_path_file=full_path_file)

    print("Process finished...")