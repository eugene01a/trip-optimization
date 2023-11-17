from sqlalchemy import Integer, String, Float, ForeignKey

from src import db


class Place(db.Model):
    __tablename__ = "places"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(40), unique=True)

    def __init__(self, name):
        self.name = name


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    place_id = db.Column(Integer, ForeignKey(Place.id))
    map_id = db.Column(String)
    latitude = db.Column(Float)
    longitude = db.Column(Float)
    address = db.Column(String(80))

    def __init__(self, place_id, map_id, latitude, longitude, address):
        self.place_id = place_id
        self.map_id = map_id
        self.latitude = latitude
        self.longitude = longitude
        self.address = address


class OpenHours(db.Model):
    __tablename__ = "opening_hours"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    location_id = db.Column(Integer, ForeignKey("locations.id"), nullable=False, unique=True)
    phone_number = db.Column(String(20), nullable=True)
    monday = db.Column(String(60), nullable=True)
    tuesday = db.Column(String(60), nullable=True)
    wednesday = db.Column(String(60), nullable=True)
    thursday = db.Column(String(60), nullable=True)
    friday = db.Column(String(60), nullable=True)
    saturday = db.Column(String(50), nullable=True)
    sunday = db.Column(String(50), nullable=True)

    def __init__(self, location_id, phone_number, monday, tuesday, wednesday, thursday, friday, saturday, sunday):
        self.location_id = location_id
        self.phone_number = phone_number
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday
