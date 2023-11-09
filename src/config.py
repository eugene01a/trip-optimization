import configparser

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['googlemaps']['api_key']

