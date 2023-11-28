import configparser
import logging

config = configparser.ConfigParser()
config.read('novi.ini')

logging.getLogger(__name__).addHandler(logging.NullHandler())
