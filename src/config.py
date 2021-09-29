import yaml
import os
PROJECT_ROOT = os.environ.get('MY_HOME', "/Users/eichinose/src/trip-optimization")
CONFIG_HOME = PROJECT_ROOT+"/etc"

def load(filename, mode = 'r'):
    config_home_path = os.path.join(CONFIG_HOME, '%s.yml' % filename )
    with open(config_home_path, 'r') as ymlfile:
        return yaml.safe_load(ymlfile)
