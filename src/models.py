# from enum import Enum
#
#
# class Day(Enum):
#     MONDAY = 0
#     TUESDAY = 1
#     WEDNESDAY = 2
#     THURSDAY = 3
#     FRIDAY = 4
#     SATURDAY = 5
#     SUNDAY = 6
#
#
# class Trip:
#     def __init__(self, day, origin, destination, depart_after, arrive_by):
#         self.day = day
#         self.origin = origin
#         self.destination = destination
#         self.depart_after = depart_after
#         self.arrive_by = arrive_by
#         self.stops = None
#
#     def add_valid_stop(self, stop):
#         pass
#
#     def remove_last_stop(self):
#         pass
#
#     def print_trip(self):
#         pass
#
#
# class TripStop:
#     def __init__(self, errand, arrival_time):
#         self.errand = errand
#         self.arrival_time = arrival_time
#         self.next = None
#
#
# class Place:
#     def __init__(self, place_id, search_name, coordinates, address):
#         self.id = place_id
#         self.search_name = search_name
#         self.coordinates = coordinates
#         self.address = address
#
#
# class Business:
#     def __init__(self, place, opening_hours, phone_number):
#         self.id = place.id
#         self.search_name = place.search_name
#         self.coordinates = place.coordinates
#         self.address = place.address
#         self.opening_hours = opening_hours
#         self.phone_number = phone_number
#
#     def is_open(self):
#         pass
