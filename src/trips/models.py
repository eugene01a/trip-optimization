from collections import namedtuple


class Origin:
    def __init__(self, address, depart_after):
        self.address = address
        self.depart_after = depart_after


class Destination:
    def __init__(self, address, arrive_by):
        self.address = address
        self.arrive_by = arrive_by


class Route:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.stops = []


'''
duration: timedelta 
'''
Errand = namedtuple("Errand", ['name', 'address', 'duration'])

class Stop:
    def __init__(self, errand, arrive_at):
        self.arrive_at = arrive_at
        self.address = errand.address
        self.depart_at = arrive_at + errand.duration
        self.errand = errand
