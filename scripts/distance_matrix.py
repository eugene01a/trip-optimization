from pprint import pprint

from src.maps import travel_time
from datetime import datetime
from datetime import datetime, timedelta

from src import config

origin="242 Keller St. Monterey Park, CA 91755"
destination = "Sunset Recycling Center Montebello"

departure_time = datetime.now() + timedelta(hours=3)

response = travel_time(origin, destination, departure_time)
pprint(response)