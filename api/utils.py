class Utils:

    def __init__(self):
        school_1 = {'lat': 40.712776, 'lon': -74.005974}
        school_2 = {'lat': 47.751076,  'lon': -120.740135}
        school_3 = {'lat': 37.774929, 'lon': -122.419418}        
        self._school_list = [school_1, school_2, school_3]

    def dist_between_two_lat_lon(self, *args):
        from math import asin, cos, radians, sin, sqrt
        lat1, lat2, long1, long2 = map(radians, args)

        dist_lats = abs(lat2 - lat1) 
        dist_longs = abs(long2 - long1) 
        a = sin(dist_lats/2)**2 + cos(lat1) * cos(lat2) * sin(dist_longs/2)**2
        c = asin(sqrt(a)) * 2
        radius_earth = 6378
        return c * radius_earth

    def find_closest_lat_lon(self, data, user_location):
        try:
            return min(data, key=lambda p: self.dist_between_two_lat_lon(user_location['lat'],
                                                        user_location['lon'],p['lat'],p['lon']))
        except TypeError:
            print('Not a list or not a number.')