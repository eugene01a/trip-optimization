class Place:
    def __init__(self, name, address):
        self.name = name
        self.address = address

class Stop(Place):
    def __init__(self, name, address, hours):
        self.hours = hours
        Place.__init__(self, name, address)

    def routeFrom(self, location):
        pass

    def isOpen(self, arrival_time):
        pass



