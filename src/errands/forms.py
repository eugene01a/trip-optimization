from wtforms import Form, StringField, validators, IntegerField

class ErrandForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    place_input = StringField('Place')
    duration_mins = IntegerField('Estimated Duration (minutes)')
    notes = StringField('Notes')
