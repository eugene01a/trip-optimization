from collections import defaultdict

import googlemaps

from src import config

secret_key = config.get_api_key()
gmaps = googlemaps.Client(key=secret_key)


def dist_matrix(origins, destinations, departure_time):
    response = gmaps.distance_matrix(origins, destinations,
                                     departure_time=departure_time,
                                     mode="driving")
    return response


def find_single_place(input):
    response = gmaps.find_place(input, input_type='textquery',
                                fields=["name",
                                        "place_id",
                                        "geometry/location",
                                        "formatted_address"
                                        ])

    candidates = response['candidates']

    if not candidates:
        raise ValueError(f"No places found for input '{input}'")

    if len(candidates) > 1:
        raise ValueError(f"More than one place found for input '{input}'" % candidates)

    candidate = candidates[0]
    location = candidate['geometry']['location']

    return {
        "search_input": input,
        "place_id": candidate.get('place_id'),
        "place_name": candidate.get('name'),
        "address": candidate.get('formatted_address'),
        "coordinates": (location.get('lat'), location.get('lng'))
    }


def format_opening_hours(raw_hours):
    '''
    input: {'periods': [{'close': {'day': 1, 'time': '1200'},
                   'open': {'day': 1, 'time': '0930'}},
                  {'close': {'day': 1, 'time': '1730'},
                   'open': {'day': 1, 'time': '1430'}},
                  {'close': {'day': 5, 'time': '1730'},
                   'open': {'day': 5, 'time': '1430'}}]}
    output: {0: [], 1: [(930,1200),(1430,1730)], 5:[(1430,1730)]}
    '''
    formatted_res = defaultdict(list)
    periods = raw_hours['periods']
    for period in periods:
        open = period['open']['time']
        close = period['close']['time']
        if period['open']['day'] != period['close']['day']:
            raise ValueError(f"open and close days are different for placeid '{period}'")
        day = period['close']['day']
        formatted_res[day].append((open, close))

    return formatted_res


def place_details(place_id):
    '''
    {'html_attributions': [],
    'result': {'formatted_phone_number': '03-3423-1200',
            'opening_hours': {'open_now': False,
                              'periods': [{'close': {'day': 1, 'time': '1200'},
                                           'open': {'day': 1, 'time': '0930'}},
                                          {'close': {'day': 1, 'time': '1730'},
                                           'open': {'day': 1, 'time': '1430'}},
                                          {'close': {'day': 2, 'time': '1200'},
                                           'open': {'day': 2, 'time': '0930'}},
                                          {'close': {'day': 2, 'time': '1730'},
                                           'open': {'day': 2, 'time': '1430'}},
                                          {'close': {'day': 3, 'time': '1200'},
                                           'open': {'day': 3, 'time': '0930'}},
                                          {'close': {'day': 3, 'time': '1730'},
                                           'open': {'day': 3, 'time': '1430'}},
                                          {'close': {'day': 4, 'time': '1200'},
                                           'open': {'day': 4, 'time': '0930'}},
                                          {'close': {'day': 4, 'time': '1730'},
                                           'open': {'day': 4, 'time': '1430'}},
                                          {'close': {'day': 5, 'time': '1200'},
                                           'open': {'day': 5, 'time': '0930'}},
                                          {'close': {'day': 5, 'time': '1730'},
                                           'open': {'day': 5, 'time': '1430'}}],
                              'weekday_text': ['Monday: 9:30\u202fAM\u2009'
                                               '–\u200912:00\u202fPM, '
                                               '2:30\u2009–\u20095:30\u202fPM',
                                               'Tuesday: 9:30\u202fAM\u2009'
                                               '–\u200912:00\u202fPM, '
                                               '2:30\u2009–\u20095:30\u202fPM',
                                               'Wednesday: 9:30\u202fAM\u2009'
                                               '–\u200912:00\u202fPM, '
                                               '2:30\u2009–\u20095:30\u202fPM',
                                               'Thursday: 9:30\u202fAM\u2009'
                                               '–\u200912:00\u202fPM, '
                                               '2:30\u2009–\u20095:30\u202fPM',
                                               'Friday: 9:30\u202fAM\u2009'
                                               '–\u200912:00\u202fPM, '
                                               '2:30\u2009–\u20095:30\u202fPM',
                                               'Saturday: Closed',
                                               'Sunday: Closed']}},
 'status': 'OK'}

    '''
    response = gmaps.place(place_id, fields=['formatted_phone_number',
                                             "opening_hours",
                                             ])

    result = response['result']
    raw_hours = result.get("opening_hours")
    opening_hours = format_opening_hours(raw_hours)

    return {
        "phone_number": result.get('formatted_phone_number'),
        "opening_hours": opening_hours
    }
