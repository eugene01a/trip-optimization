import json
import googlemaps

from src import config
import urllib
auth = config.load('config')


def distance(start, end, units='imperial'):
    key = auth['googlemaps']['distance']
    gmaps = googlemaps.Client(key=key)
    response =  gmaps.distance_matrix(start, end, units=units)
    # print response
    return response['rows'][0]['elements'][0]['distance']['value']

def miles_to_meters(miles):
    conversion_factor = 1609.34
    return round(miles * conversion_factor,2)


def meters_to_miles(meters):
    return round(meters / 1609.344,2)


# find the total distance traveled on a given route, default units is meters
def total_distance(directions):
    distance = 0
    for leg in directions[0]['legs']:
        distance += leg['distance']['value']
    return distance

def total_distance_miles(result):
    distance_meters = result[0]['distance']['value']
    return meters_to_miles(distance_meters)

def total_duration(result):
    return result[0]['duration']['value']

def directions(start, end, stops=None):
    key = auth['googlemaps']['directions']
    gmaps = googlemaps.Client(key=key)
    result = gmaps.directions(start, end, waypoints=stops)
    return result

def nearby(address, radius, **kwargs):
    geocode_key = auth['googlemaps']['geocoding']
    geocode = googlemaps.Client(key=geocode_key)
    coordinates = geocode.geocode(address=address)[0]['geometry']['location']
    key = auth['googlemaps']['places']
    places = googlemaps.Client(key=key)
    response = places.places_nearby(coordinates, radius=radius, **kwargs)
    for result in response['results']:
        print(result)
    return response['results']


def extract_nearby_place_ids(result):
    place_ids = []
    for place in result:
        place_ids.append(place['place_id'])
    return place_ids


def lookup_id_in_results(id, result):
    for place in result:
        if place['place_id'] == id:
            return place


def display_results(result):
    print (json.dumps(result, indent=4))


# check if a place is on the way between an origin and destination
def check_on_route(start, end, route_dist, tolerance, place):
    route_directions = directions(start,end,stops = place)
    distance_combined = total_distance(route_directions)
    # check that adding the stop to the route doesnt increase the total distance travelled by more than the tolerance.
    if distance_combined - tolerance <= route_dist:
        return True
    return False


def filter_stops(route, places, tolerance):
    '''
    filter and order places along existing route with specified tolerance
    '''
    original_distance = total_distance(route)
    optimized_locations = []

    # loop through each place
    for place in places:

        # check number of legs in the route
        n_legs = len(route[0]['legs'])
        # define start as the start location of the first leg of the route
        start = route[0]['legs'][0]['start_address']
        # define end as the end location of the last leg of the route
        end = route[0]['legs'][n_legs - 1]['end_address']

        # if more than one leg in route loop through each
        if n_legs > 1:
            for leg in route[0]['legs']:
                # check if place is on the way between start and end location of leg
                leg_start, leg_end = leg['start_address'], leg['end_address']
                on_way = check_on_route(leg_start, leg_end, original_distance, tolerance)
                if on_way:
                    optimized_locations.append(place)
                    print(place)
                    break

        else:
            on_way = check_on_route(start, end, place, tolerance)
            if on_way:
                optimized_locations.append(place)
                route = directions(start, end, stops=places)
                print (place)
    print(optimized_locations)
    return optimized_locations


def optimize_stop(start, end, stops, tolerance):
    route = directions(start, end)
    stops = filter_stops(route, stops, tolerance)
    return directions(start, end, stops)

def extract_nearby_placeids(result):
    place_ids = []
    for place in result:
        place_ids.append(place['place_id'])
    return place_ids

def lookup_id_in_results(id, result):
    for place in result:
        if place['place_id'] == id:
            return place

def nearby_route_search(start, end, radius_factor=1, **kwargs):
    route_dist = distance(start, end)
    radius = radius_factor * route_dist
    nearby_start = nearby(start, radius, **kwargs)
    nearby_end = nearby(end, radius, **kwargs)

    common_ids = list(set(extract_nearby_placeids(nearby_start))  & set(extract_nearby_place_ids(nearby_end)))
    common_places = []
    common_coordinates = []
    for common_id in common_ids:
        place = lookup_id_in_results(common_id, nearby_start)
        common_places.append(place)
        common_coordinates.append(place['geometry']['location'])
    return (common_coordinates, common_places, route_dist)

def lookup_place_by_coordinates(coordinates,places):
    for place in places:
        if place['geometry']['location'] == coordinates:
            return place

def filter_along_route(start, end, tolerance_miles, **kwargs):
    (coordinates, places, original_distance) = nearby_route_search(start, end, **kwargs)
    tolerance = miles_to_meters(tolerance_miles)
    on_the_way = []
    original_dist = str(meters_to_miles(original_distance))+" miles"
    for coordinate in coordinates:
        if check_on_route(start, end, original_distance, tolerance,coordinate):
            place = lookup_place_by_coordinates(coordinate, places)
            place['original_distance'] = original_distance
            on_the_way.append(place)
            print ('\n', place['name'])
            print (place['vicinity'])
            total_dist = total_distance(directions(start,end,stops=[coordinate]))
            print ("New distance ", meters_to_miles(total_dist), " miles")
            place['new_distance'] = str(meters_to_miles(total_dist))+" miles"
    return original_dist, on_the_way

def make_directions_url(origin, destination, waypoint):
    '''
    Summary:
    returns a properly encoded url to launch src directions

    Reference:
    https://developers.google.com/maps/documentation/urls/guide
    '''
    params = {
        'origin': origin,
        'destination': destination,
        'travelmode': 'driving',
        'dir_action': 'navigate',
        'waypoints': waypoint
    }
    base_url = "https://www.google.com/maps/dir/?api=1&"
    url_params = urllib.urlencode(params)

    return base_url + url_params

class SearchRoute:
    def __init__(self):
        key = auth['googlemaps']['distance']
        self.client = googlemaps.Client(key=key)

    def distance(start, end, units='imperial'):

        response = gmaps.distance_matrix(start, end, units=units)
        print(response)
        return response['rows'][0]['elements'][0]['distance']['value']




