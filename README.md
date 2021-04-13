# API_geocode
* to install, pip3 install pipenv
pipenv shell (EN EL DIRECTORIO DONDE ESTA EL REQUIREMENTS)
una vez iniciado su entorno virtual:
pipenv install -r requirements.txt


para iniciar el app
python main.py

 ** acabo de hacer esta estructura/distribucion** los imports de cada file no van a funcionar
# REQUEST

GET /api/eta-closest-hs?lat=xx&long=xx


# RESPONSE

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
``` 

# downloads contiene los csvs (miguel los va a remplazar)
-> scripts para crear de CSVs a Mongo, y para agregarle a un CSV su geocodes segun el address

# en API tenemos toda la aplicacion
-> controllers hacen toda la interaccion y logica con los models
-> models solo definen objetos y solo ellos mismos se pueden cambiar (payload en su def dict se genera la respuesta del API)
-> street viewers es quien habla con google (hay otros llamados de google en utils y controllers must refactor)
-> utils tiene todas las funciones necesarias para la aplicacion

# cache 
-> aqui va a ver un cache de todos los request que se han hecho
-> se devuelve la misma respuesta si el mismo geocode hace una consulta
-> se devuelve el mismo DRONE ID si el request esta en el ratio de 2miles de las respuestas en cache
-> debemos eventualmente guardar las imagenes y dejar de consultar a google por cada una

# chart-values 
-> API key (not actually being used now)

# scripts 
-> tiene el primer API que se hizo, se mantienen los files

# static
-> varios JSONs a differentes llamados del API, o ya sea objetos del programa para ver su estructura

# test
-> TO-DO unit testing of all API

