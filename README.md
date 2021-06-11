# API_geocode
with a virtual env, install requirements.txt
then run main.py
# REQUEST
 
POST /safewrd/
```
        {
        "geocodes": [26.2078509, -80.1427387],
        "uid": "CA308008-421B-11EB-B2BF-EDEFCE1D72FE",
        "size": "600x800"
        }

```

# RESPONSE
``` 

{
    "user_data": "CA308008-421B-11EB-B2BF-EDEFCE1D72FE",
    "user_location": [
        26.2078509,
        -80.1427387
    ],
    "date_of_request": "2021-04-25 20:22:06.692469",
    "payload_id": "1_safewrd_vwmReCr8",
    "drone": {
        "drone_id": 1,
        "drone_speed": "0.51 ml/h"
    },
    "miles_distance": "0.69 miles",
    "estimated_time": "1.33 minutes",
    "embedded_map": "<iframe width=\"600\" height=\"500\" id=\"gmap_canvas\" src=\"https://maps.google.com/maps?q=6000%20NE%209th%20Ave%2C%20Fort%20Lauderdale%2C%20FL%2033334%2C%20USA&t=&z=13&ie=UTF8&iwloc=&output=embed\" frameborder=\"0\" scrolling=\"no\" marginheight=\"0\" marginwidth=\"0\"></iframe>",
    "nearest_school": {
        "name": "Broward County Public S...",
        "address": "6000 NE 9th Ave, Fort Lauderdale, FL 33334, USA",
        "geocodes": {
            "lat": 26.2019092,
            "lon": -80.1338845
        },
        "school_image": "https://maps.googleapis.com/maps/api/streetview?size=600x800&location=6000%20NE%209th%20Ave%2C%20Fort%20Lauderdale%2C%20FL%2033334%2C%20USA&key=AIzaSyDyn3nhSkxdxS6aUJXim4O-T50ZtLg4YGY"
    },
    "aireos_vote_url": "https://www.aireos.io/network/"
}
``` 


``` 
# Default server configuration
#
server {
        listen 80 default_server;
        listen [::]:80 default_server;


        root /var/www/html/git;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ =404;
        }

location ~ (/.*) {
    client_max_body_size 0; # Git pushes can be massive, just to make sure nginx doesn't suddenly cut the connection add this.
    auth_basic "Git Login"; # Whatever text will do.
    auth_basic_user_file "/var/www/html/git/htpasswd";
    include /etc/nginx/fastcgi_params; # Include the default fastcgi configs
    fastcgi_param SCRIPT_FILENAME /usr/lib/git-core/git-http-backend; # Tells fastcgi to pass the request to the git http backend executable
    fastcgi_param GIT_HTTP_EXPORT_ALL "";
    fastcgi_param GIT_PROJECT_ROOT /var/www/html/git; # /var/www/git is the location of all of your git repositories.
    fastcgi_param REMOTE_USER $remote_user;
    fastcgi_param PATH_INFO $1; # Takes the capture group from our location directive and gives git that.
    fastcgi_pass  unix:/var/run/fcgiwrap.socket; # Pass the request to fastcgi
}

}