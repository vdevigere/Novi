import configparser
import logging

config = configparser.ConfigParser()
config.read('okapi.ini')

logging.getLogger(__name__).addHandler(logging.NullHandler())
