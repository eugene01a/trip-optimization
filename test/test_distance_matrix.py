import pprint
from datetime import datetime

from src.maps import dist_matrix

origins = "242 Keller St. Monterey Park, CA 91755"
destinations = ["Home Depot Monterey Park",
                "Walmart Rosemead",
                "Costco Monterey Park"]

departure_time = datetime.now()

response = dist_matrix(origins=origins,
                       destinations=destinations,
                       departure_time=departure_time)

pprint.pp(response)