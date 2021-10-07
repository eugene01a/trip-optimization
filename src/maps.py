import json
import urllib

import googlemaps

from src import config

credentials = config.load('auth')
secret_key=credentials['googlemaps']

gmaps = googlemaps.Client(key=secret_key)

def dist_matrix(origin, dest, departure_time):
    response = gmaps.distance_matrix(origin, dest, departure_time = departure_time)
    return response




