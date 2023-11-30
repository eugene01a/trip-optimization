class Trip:
    def __init__(self, day, origin, destination, depart_by, arrive_by):
        self.day = day
        self.origin = origin
        self.destination = destination
        self.depart_by = depart_by
        self.arrive_by = arrive_by
        self.stops = None

    def add_valid_stop(self, stop):
        pass

    def remove_last_stop(self):
        pass

    def print_trip(self):
        pass


class TripStop:
    def __init__(self, errand, arrival_time):
        self.errand = errand
        self.arrival_time = arrival_time
        self.next = None