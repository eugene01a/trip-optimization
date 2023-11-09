from collections import defaultdict

from src.models import Business, Place
from src.wrappers import find_single_place, place_details


def format_opening_hours(raw_hours):
    '''
    {'open_now': False,
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


def create_place(input):
    place_response = find_single_place(input)
    return Place(place_response['place_id'],
                 place_response['search_input'],
                 place_response['coordinates'],
                 place_response['address'])


def create_business(input):
    place = create_place(input)
    details_response = place_details(place.id)
    return Business(place,
                    details_response['opening_hours'],
                    details_response['phone_number'])
