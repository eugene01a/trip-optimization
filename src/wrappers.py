import json
from collections import defaultdict
from enum import Enum

import googlemaps

from src import config, db
from src.places.models import Location, Place, OpenHours

secret_key = config.get_api_key()
gmaps = googlemaps.Client(key=secret_key)


class Day(Enum):
    sunday = 0
    monday = 1
    tuesday = 2
    wednesday = 3
    thursday = 4
    friday = 5
    saturday = 6


def dist_matrix(origins, destinations, departure_time):
    response = gmaps.distance_matrix(origins, destinations,
                                     departure_time=departure_time,
                                     mode="driving")
    return response


def add_new_place(place_input):
    """
    Finds the location of a place and adds it to the Location and Place db tables

    input:
    place_input = UNIQUE PLACE NAME THAT DOES NOT YET EXIST IN THE PLACES TABLE

    output:
    newly created Place and Location objects
    """
    response = gmaps.find_place(place_input, input_type='textquery',
                                fields=["name",
                                        "place_id",
                                        "geometry/location",
                                        "formatted_address"
                                        ])

    candidates = response['candidates']

    if not candidates:
        raise ValueError(f"No places found for input '{place_input}'")

    if len(candidates) > 1:
        raise ValueError(f"More than one place found for input '{place_input}'" % candidates)

    # Add place into table
    place = Place(place_input)
    db.session.add(place)
    db.session.commit()

    candidate = candidates[0]

    location = Location(place_id=place.id,
                        map_id=candidate.get('place_id'),
                        latitude=candidate['geometry']['location']['lat'],
                        longitude=candidate['geometry']['location']['lng'],
                        address=candidate.get('formatted_address')
                        )

    db.session.add(location)
    db.session.commit()

    return place, location


def format_raw_hours(raw_hours):
    """
    Raw hours from googlemaps api are in the following format:
    [{'close': {'day': 1, 'time': '1200'}, 'open': {'day': 1, 'time': '0930'}},
    {'close': {'day': 1, 'time': '1730'}, 'open': {'day': 1, 'time': '1430'}},
    {'close': {'day': 2, 'time': '1200'}, 'open': {'day': 2, 'time': '0930'}},
    {'close': {'day': 2, 'time': '1730'}, 'open': {'day': 2, 'time': '1430'}},
    {'close': {'day': 3, 'time': '1200'}, 'open': {'day': 3, 'time': '0930'}},
    {'close': {'day': 3, 'time': '1730'}, 'open': {'day': 3, 'time': '1430'}},
    {'close': {'day': 4, 'time': '1200'}, 'open': {'day': 4, 'time': '0930'}},
    {'close': {'day': 4, 'time': '1730'}, 'open': {'day': 4, 'time': '1430'}},
    {'close': {'day': 5, 'time': '1200'}, 'open': {'day': 5, 'time': '0930'}},
    {'close': {'day': 5, 'time': '1730'}, 'open': {'day': 5, 'time': '1430'}}]

    """
    formatted_res = defaultdict(list)
    periods = raw_hours['periods']
    print(f"DEBUG: periods={periods}")
    for period in periods:
        open_time = period['open']['time']
        open_day = period['open']['day']
        close_time = period['close']['time']
        close_day = period['close']['day']
        if open_day != close_day:
            raise ValueError(f"open and close days are different for period '{period}'")

        p = (open_time, close_time)
        weekday = Day(open_day).name
        formatted_res[weekday].append(json.dumps(p))
    return formatted_res


def add_opening_hours(location):
    """
    Finds the location of a place and adds it to the Location and Place db tables

    input:
    location = Location object in DB

    output:
    newly created OpenHours object
    """

    response = gmaps.place(location.map_id, fields=['formatted_phone_number',
                                                    "opening_hours",
                                                    ])
    result = response['result']
    raw_hours = result.get("opening_hours")

    open_hours = OpenHours(location.id,
                           phone_number=result.get('formatted_phone_number'),
                           **format_raw_hours(raw_hours))

    db.session.add(open_hours)
    db.session.commit()

    return open_hours
