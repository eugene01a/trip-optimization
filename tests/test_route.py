from lib.maps import *

start = '1600 Amphitheatre Parkway Mountain View, CA 94043'
end = '1 Apple Park Way Cupertino, California, United States'
query = {
    'name': 'supermarket'
}
# max distance from route in miles
tolerance = 1

response = filter_along_route(start, end, tolerance, **query)
