import pandas as pd
import os
import json
from api.street_view import StreetViewer


class StoreImage:
    def __init__(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.location = __location__
        self.cwd = os.path.realpath(os.path.join(os.getcwd()))
        self.df = self._read_csv_data()
        self.image_data = {}
        self.image_empty_data = {}

    def _read_csv_data(self):
        csv_file_path = "{0}/schools.csv".format(self.cwd)
        csv_df = pd.read_csv(csv_file_path)
        return csv_df

    def check_file_exists(self, file_path):
        if os.path.exists(file_path) is False:
            with open(file_path, "w") as file:
                file.close()

    def process_data(self):
        total = 17405
        first, bound = 0, 17404
        for index in range(first, bound):
            print("Current index: {0}".format(str(index)))
            print(self.df.iloc[index]['FullAddress'])
            street_view = StreetViewer(location=self.df.iloc[index]['FullAddress'])
            image_path = street_view.get_picture()
            print(image_path)
            if image_path is None:
                website = self.df.iloc[index]['WEBSITE']
                self.image_empty_data[index] = website if website else ""
                continue
            self.image_data[index] = image_path

            self._store_json_data()

    def _store_json_data(self):
        self.check_file_exists("{0}/image_json_data.json".format(self.cwd))
        self.check_file_exists("{0}/image_none_data.json".format(self.cwd))
        with open("{0}/image_json_data.json".format(self.cwd), "r+") as file:
            data = file.readlines()
            file.seek(0)
            file.truncate()
            data_dict = {} if len(data) == 0 else json.loads(data[-1])
            data_dict.update(self.image_data)
            json.dump(data_dict, file)
            file.close()

        with open("{0}/image_none_data.json".format(self.cwd), "r+") as file:
            data = file.readlines()
            file.seek(0)
            file.truncate()
            data_dict = {} if len(data) == 0 else json.loads(data[-1])
            data_dict.update(self.image_empty_data)
            json.dump(data_dict, file)
            file.close()


