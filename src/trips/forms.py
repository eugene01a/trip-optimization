from wtforms import Form, TimeField, StringField, DateField


class TripForm(Form):
    day = DateField("Date")
    origin = StringField("Origin")
    destination = StringField("Destination")
    depart_by = TimeField("Latest departure time")
    arrive_by = TimeField("Latest arrival time")
