import requests
import os
import json
import shortuuid

class StreetViewer(object):
    def __init__(self, location = ''):
        __location__ = os.path.realpath(  # use this to make current directory reference can be changed
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
        
        self._key = 'AIzaSyCL3WravFN_wNUfKU6cC4QRWAOzfbfo49g' # to be readed from values.yaml w/ os.environ()

        self.size = "640x640"
        self.folder_directory = __location__ + '/saved-images/'

        self.location = location # ADDRESS

        self._meta_params = dict(key=self._key,
                                location=self.location)
        self._pic_params = dict(key=self._key,
                               location=self.location,
                               size=self.size)

        self.meta_status = {} # to be use to ask for the image

        self._id =  shortuuid.uuid()


    
    def get_meta(self):
        """
        Method to query the metadata of the address to then save the image
        """
        # saving the metadata as json for later usage
        meta_name = "meta_{}.json".format(self._id)

        # hit google api for metadata of an address
        meta_response = requests.get(
            'https://maps.googleapis.com/maps/api/streetview/metadata?',
            params=self._meta_params)

        meta_info = meta_response.json()

        # meta_status is used in get_pic method to avoid ask for not available pictures
        self.meta_status = meta_info['status']

        if meta_response.ok:
            print(">>> Obtained Meta from StreetView API:")
            print(meta_info)
            with open(meta_name, 'w') as file:
                json.dump(meta_info, file)
        else:
            print(">>> Failed to obtain Meta from StreetView API!!!")
            meta_response.close()
    
    def save_pic(self):
        """
        Method to query the StreetView picture and save to local directory
        """
        # define path to save picture and headers
        pic_path = "pic_{}.jpg".format(self._id)
        header_path = "header_{}.json".format(self._id)
        # only when meta_status is OK will the code run to query picture (cost incurred)
        if self.meta_status == 'OK':
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
        else:
            print(">>> Picture not available in StreetView!")

    def get_picture(self):
        """ getting the picture can be done from here? or not-- 
        maybe utils - or from a controller depending on where will be needed"""
        pass


testing_street_viewer = StreetViewer(location='7930 W 26th St, North Riverside, IL 60546, United States')
testing_street_viewer.get_meta()
testing_street_viewer.save_pic()