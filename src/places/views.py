from flask import Blueprint, request, render_template

'''
A Blueprint is a way to organize a group of related views and other code. 
Rather than registering views and other code directly with an application, they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
'''

bp = Blueprint('place', __name__)

@bp.route('/places/create', methods=('GET', 'POST'))
def places_create():
    pass