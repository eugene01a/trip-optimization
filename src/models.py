from src import db


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, name, location, hours):
        self.name = name
        self.location = location
        self.hours = hours


class Errand(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place_id = db.Column(db.Integer, db.ForeignKey("registration.id"))

    def __init__(self, name, place_id, duration):
        self.name = name
        self.place_id = place_id
        self.duration = duration
