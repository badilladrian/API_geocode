import requests
import os
import json
import shortuuid


class StreetViewer(object):
    def __init__(self, location=''):
        __location__ = os.path.realpath(
            # use this to make current directory reference can be changed
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        self._key = 'AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g'  # to be readed from values.yaml w/ os.environ()

        self.size = "640x640"
        self.folder_directory = __location__ + '/saved-images/'
        self.base_path = __location__

        self.location = location  # ADDRESS

        self._meta_params = dict(key=self._key,
                                 location=self.location)
        self._pic_params = dict(key=self._key,
                                location=self.location,
                                size=self.size)

        self.meta_status = {}  # to be use to ask for the image

        self._id = shortuuid.uuid()

    def check_exists_folder(self, folder_path):
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

    def check_exists_file(self, file_path):
        return True if os.path.isfile(file_path) else False

    def get_meta(self):
        """
        Method to query the metadata of the address to then save the image
        """
        # saving the metadata as json for later usage
        meta_name = self.folder_directory + "meta_{}.json".format(self._id)
        print(self._meta_params)

        # hit google api for metadata of an address
        meta_response = requests.get(
            'https://maps.googleapis.com/maps/api/streetview/metadata?',
            params=self._meta_params)

        meta_info = meta_response.json()

        # meta_status is used in get_pic method to avoid ask for not available pictures
        self.meta_status = meta_info['status']

        if meta_response.ok:
            if self.meta_status == "ZERO_RESULTS":
                meta_info['pano_id'] = "ZERO_RESULTS-" + self.location
            json_file_path = self.folder_directory + "meta_{0}.json".format(
                meta_info['pano_id'])
            if self.check_exists_file(json_file_path):
                return meta_info
            print(">>> Obtained Meta from StreetView API:")
            meta_name = json_file_path
            with open(meta_name, 'w') as file:
                json.dump(meta_info, file)
            return meta_info
        else:
            print(">>> Failed to obtain Meta from StreetView API!!!")
            meta_response.close()
            return None

    def save_pic(self, meta_info):
        """
        Method to query the StreetView picture and save to local directory
        """
        # define path to save picture and headers
        self.check_exists_folder(self.folder_directory)
        pic_path = self.folder_directory + "pic_{}.jpg".format(meta_info['pano_id'])
        header_path = self.folder_directory + "header_{}.json".format(meta_info['pano_id'])
        # only when meta_status is OK will the code run to query picture (cost incurred)
        if self.meta_status == 'OK' or self.meta_status == 'ZERO_RESULTS':
            print(">>> Picture available, requesting now...")

            _pic_response = requests.get(
                'https://maps.googleapis.com/maps/api/streetview?',
                params=self._pic_params)

            pic_header = dict(_pic_response.headers)

            if _pic_response.ok:
                print(f">>> Saving Picture Data to {self.folder_directory}")

                with open(pic_path, 'wb') as file:
                    file.write(_pic_response.content)

                with open(header_path, 'w') as file:
                    json.dump(pic_header, file)

                _pic_response.close()
                print(">>> COMPLETE!")
                return pic_path
        else:
            print(">>> Picture not available in StreetView!")
            return None

    def get_picture(self):
        """ getting the picture can be done from here? or not--
        maybe utils - or from a controller depending on where will be needed"""
        meta_info = self.get_meta()
        if meta_info is not None:
            pano_id = meta_info['pano_id']
            pic_path = self.folder_directory + "pic_{}.jpg".format(pano_id)
            if self.check_exists_file(pic_path):
                print(">>> Picture exists!")
                return pic_path
            else:
                pic_path = self.save_pic(meta_info)
                return pic_path
