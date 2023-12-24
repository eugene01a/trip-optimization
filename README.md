# trip-optimization
A route planning application for running errands.

### Setup
All steps below are done from the root of the project.
Create your own _.env_ file:
```ini
# .env
DB_USERNAME={YOUR_USERNAME}
DB_PASSWORD= {YOUR_PASSWORD}
DB_NAME= {YOUR_DB_NAME}
```

Create a file named _config.ini_:
```ini
# config.ini
[googlemaps]
api_key={YOUR_API_KEY_FROM_GOOGLE}
```

Create the docker containers for postgres and adminer (DB admin tool):
```commandline
docker-compose up -d
```

Add this environment variable to your bashrc or zshrc file:
```commandline
export FLASK_APP=src/__init__.py
```

Initialize the database schema:
```commandline
flask init-db
```

Verify by logging into the adminer portal at
http://localhost:8080/

Finally, run the flask app:
```commandline
flask run
```

