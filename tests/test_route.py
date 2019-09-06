from lib.maps import *
start = '8356 Garibaldi Ave. 91775'
end = '242 Keller St. 91755'
query = {
    'name': 'supermarket'
}
# max distance from route in miles
tolerance = 1

response = filter_along_route(start, end, tolerance, **query)
