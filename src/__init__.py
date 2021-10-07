# auth/server/__init__.py

import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'trip_optimization.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/trip_optimization_server.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('TripOptimization startup')
