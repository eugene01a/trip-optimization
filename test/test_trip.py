from datetime import timedelta
from enum import Enum


class CalcType(Enum):
    ANY = 0
    ON_TIME = 1
    BEFORE = 2
    AFTER = 3


class OriginInfo:
    def __init__(self, location, time, calc_type):
        self.location = location
        self.time = time
        self.calc_type = calc_type

    def on_schedule(self, time):
        pass

class DestinationInfo:
    def __init__(self, location, time, calc_type):
        self.location = location
        self.time = time
        self.calc_type = calc_type

    def on_schedule(self, time):
        pass


class StopInfo:
    def __init__(self, description, location, duration, notes=[]):
        self.description = description
        self.location = location
        self.duration = duration
        self.notes = notes

    def is_open(self, arrival_time):
        pass

    def depart_at(self, arrival_time):
        pass


class TripInfo:
    def __init__(self, date, origin_info, destination_info):
        self.date = date
        self.origin_info = origin_info
        self.destination_info = destination_info
        self.stops = []

    def check_stop(self, stop):
        pass

    def add_stop(self, stop):
        pass


origin = "242 Keller St. Monterey Park, CA 91755"
destination = "8356 E. Garibaldi Ave. San Gabriel, CA 91775"

trip_info = TripInfo("10/01/2021",
                     OriginInfo(origin, None, CalcType.ANY),
                     DestinationInfo(destination, "06:00 PM", CalcType.BEFORE))

errands = [
    {
        "description": "Refill gas",
        "location": {
            "name": "Costco Gasoline",
            "address": "2000 Market Place Dr Monterey Park, CA 91755"
        },
        "duration": timedelta(minutes=30)
    },
    {
        "description": "Return leaf blower",
        "location": {
            "name": "Harbor Freight",
            "address": None
        },
        "duration": timedelta(minutes=10)
    },
    {
        "description": "Buy stamps",
        "location": {
            "name": "US Post Office",
            "address": None
        },
        "duration": timedelta(minutes=10)
    },
    {
        "description": "Shop Tozai market",
        "location": {
            "name": "Tozai Foods Market",
            "address": "1326 Potrero Grande Dr Rosemead, CA 91770"
        },
        "duration": timedelta(minutes=15),
        "notes": ["calpis concentrate", "tsukemono"]
    },
    {
        "description": "Get Ginko Cuttings",
        "location": {
            "address": "137 Country Club Dr. San Gabriel, CA 91775",
        },
        "duration": timedelta(minutes=5),
        "notes": ["Bring pruning shears"]
    },
    {}
]
