# API_geocode

# REQUEST

GET /api/eta-closest-hs?lat=xx&long=xx


# RESPONSE

``` 
{
		"drone_id": "NYC-001",
		"ETA": "1h 37min 34sec",
		"nearest_school":
			{
				"address": "school_address",   str
 				"geocodes": [lat & long],      List<int>
				"image": image_url             str
            }
}
