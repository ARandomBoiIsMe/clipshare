import configparser

def load_config():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        return config
    except configparser.Error():
        raise