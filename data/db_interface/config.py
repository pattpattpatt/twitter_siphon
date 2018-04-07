import configparser
from data.db_interface import __credential_file__


config_file = configparser.ConfigParser()
config_file.read(__credential_file__)



