try:
    from pymongo import MongoClient
    import os
    import csv
    from pathlib import Path
except Exception as e:
    print("Some Modules are Missing ")


class MongoDB:
    def __init__(self, db_name, collection_name, host, port, file_path, inserting_batch, max_pool_size=50):
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = MongoClient(host, port, maxPoolSize=max_pool_size)
        self.data = self.client.large_data.data
        self.file_path = file_path
        self.DB = self.client[self.db_name]
        self.collection = self.DB[self.collection_name]
        self.inserting_batch = inserting_batch

    def load_data_to_mongo(self, full_path_file):
        with open(full_path_file, "r", encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            csv_reader_list = list(csv_reader)
            for value in range(0, len(csv_reader_list), self.inserting_batch):
                self.collection.insert_many(csv_reader_list[value:value + self.inserting_batch], ordered=False)
            csv_file.close()


if __name__ == '__main__':

    settings = {
        'host': 'localhost',
        'port': 27017,
        'file_path': 'C:\\Users\\migue\\Desktop\\US_School_Database\\',
        'inserting_batch': 100000,
        'db_name': 'us_school',
        'collection_name': 'School_Data'
    }

    # here we have to create the mongoDB connection using the dictionary for the settings
    mongodb = MongoDB(**settings)

    # we want to drop the collection, because we want the fresh data that is in the csv files.
    mongodb.collection.drop()

    print("Saving data in the database.... ")
    files_list = os.listdir(mongodb.file_path)
    for file in files_list:
        if file.endswith('.csv'):
            full_path_file = mongodb.file_path + file
            mongodb.load_data_to_mongo(full_path_file=full_path_file)

    print("Process finished...")