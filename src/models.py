from src import db


class Place(db.Model):
    def __init__(self, name, location, hours):
        self.name = name
        self.location = location
        self.hours = hours

class Errand(db.Model):
    def __init__(self, name, place, duration):
        self.name = name
        self.place = place

