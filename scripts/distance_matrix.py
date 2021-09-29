from pprint import pprint

import googlemaps
from datetime import datetime

from src import config

credentials = config.load('auth')
secret_key=credentials['googlemaps']

gmaps = googlemaps.Client(key=secret_key)

now = datetime.now()

destinations = [
    "Sunset Recycling Center Montebello"]

directions_result = gmaps.distance_matrix(
    "242 Keller St. Monterey Park, CA 91755",
    destinations,
    departure_time=now)

pprint(directions_result)