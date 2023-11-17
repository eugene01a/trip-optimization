import configparser


def get_sqlalchemy_uri():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['sql']['host']

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['googlemaps']['api_key']


