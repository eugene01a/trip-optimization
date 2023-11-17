from flask import Blueprint, request, render_template

from src import db
from src.errands.forms import ErrandForm
from src.errands.models import Errand
from src.places.models import Place, Location
from src.wrappers import add_new_place, add_opening_hours

'''
A Blueprint is a way to organize a group of related views and other code. 
Rather than registering views and other code directly with an application, they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
'''

bp = Blueprint('errand', __name__)


@bp.route('/errands/create', methods=('GET', 'POST'))
def errands_create():
    form = ErrandForm(request.form)
    if request.method == 'POST':
        print(f'DEBUG form={form.data}')

        place_name = form.place_input.data
        place = Place.query.filter_by(name=place_name).first()
        if not place:
            place, location = add_new_place(place_name)
            open_hours = add_opening_hours(location)


        errand = Errand(form.name.data, form.duration_mins.data, place.id, form.notes.data)
        db.session.add(errand)
        db.session.commit()

    return render_template('errand.html', form=form)
