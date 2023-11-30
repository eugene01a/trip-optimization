from src import db
from src.places.models import Place

class Errand(db.Model):
    __tablename__ = "errands"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place_id = db.Column(db.Integer, db.ForeignKey(Place.id))
    duration_mins = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(40))
    notes = db.Column(db.String(300))
    completed = db.Column(db.Boolean)

    def __init__(self, name, duration_mins, place_id, notes):
        self.name = name
        self.duration_mins = duration_mins
        self.place_id = place_id
        self.notes = notes
        self.completed = False

