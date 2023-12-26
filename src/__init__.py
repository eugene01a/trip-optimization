import os

import click
from dotenv import dotenv_values
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
from src.places.models import Place, Location

__version__ = (1, 1, 0, "dev")


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app)

    config = dotenv_values(".env")
    username = config.get("DB_USERNAME")
    password = config.get("DB_PASSWORD")
    dbname = config.get("DB_NAME")
    print(username)
    db_url = f"postgresql+psycopg://{username}:{password}@localhost:5432/{dbname}"
    app.config.from_mapping(
        # default secret that should be overridden in environ or config
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=db_url,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # initialize Flask-SQLAlchemy and the init-db command
    db.init_app(app)
    app.cli.add_command(init_db_command)

    # apply the blueprints to the app
    from src import errands, trips, places
    app.register_blueprint(errands.bp)
    app.register_blueprint(trips.bp)
    app.register_blueprint(places.bp)

    # make "index" point at "/", which is handled by "blog.index"
    app.add_url_rule("/", endpoint="")

    return app


def init_db():
    db.drop_all()
    db.create_all()
    add_fav_places()


def add_fav_places():
    home = Place("Home")
    db.session.add(home)
    home_loc = Location(home.id, "ChIJL2ax_O_PwoARkSiLOxz_TIo", 34.0460711, -118.1256168,
                        "242 Keller St. Monterey Park, CA 91755 USA")

    db.session.add(home_loc)
    db.session.flush()
    db.session.commit()



@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")
