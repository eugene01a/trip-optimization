import argparse
import pprint
import sys
from pprint import pprint
from urllib.error import HTTPError
from datetime import datetime, timedelta
from src.yelp import get_business, search, normalize_hours, is_open
from pprint import pprint

DEFAULT_TERM = 'The Joint Chiropractic'
DEFAULT_LOCATION = '242 Keller St. Monterey Park, CA'
SEARCH_LIMIT = 1


response = search(DEFAULT_TERM, DEFAULT_LOCATION, SEARCH_LIMIT)
pprint(response)

business_id = response['businesses'][0]['id']
response = get_business(business_id)
pprint(response)
normalized_hours = normalize_hours(response)
pprint(normalized_hours)

arrival_dt = datetime.now() + timedelta(days=3)
isOpen = is_open(normalized_hours, arrival_dt)
print("arrival_day: {}".format(arrival_dt.strftime("%w")))
print("arrival_time: {}".format(arrival_dt.strftime("%H%M")))
print("is open: {}".format(isOpen))