from __future__ import print_function
from urllib.parse import quote
import requests
from datetime import datetime
from collections import defaultdict
from src import config

credentials = config.load('auth')
API_KEY=credentials['yelp']

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Defaults for our simple example.
cached_hours={}
cached_ids={}
def request(host, path, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(term, location, search_limit):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': search_limit
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)
    
def normalize_hours(response):
    '''
    Original Response structure:
    https://www.yelp.com/developers/documentation/v3/business

    return dict where keys is integer enum of weekday,
    values is list of tuples represented open,close times.
    defaults to empty list if no key exists.
    '''
    hours = response['hours'][0]['open']
    normalized_hours = defaultdict(list)
    for hour in hours:
        day = hour['day']
        normalized_hours[day].append(
            (hour['start'],hour['end']))
    return normalized_hours

def is_open(normalized_hours, arrival_dt):
    day_str = arrival_dt.strftime("%w")
    arrival_time = arrival_dt.strftime("%H%M")
    for (start, end) in normalized_hours[int(day_str)]:
        if start < arrival_time < end:
          return True
    return False

        



          