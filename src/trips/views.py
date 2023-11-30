from flask import Blueprint, request, render_template

from src import db
from src.trips.forms import TripForm
from src.errands.models import Errand
from src.places.models import Place, Location
from src.wrappers import add_new_place, add_opening_hours

'''
A Blueprint is a way to organize a group of related views and other code. 
Rather than registering views and other code directly with an application, they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
'''

bp = Blueprint("trips", __name__)


@bp.route('/trip/create', methods=('GET', 'POST'))
def trip_create():
    form = TripForm(request.form)
    if request.method == 'POST':
        print(f'DEBUG form={form.data}')
    return render_template('trip.html', form=form)


