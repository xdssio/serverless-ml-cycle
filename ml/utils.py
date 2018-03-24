import json
import logging
import os

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

zappa_settings_file = 'zappa_settings.json'

with open(zappa_settings_file, 'r') as f:
    settings = json.load(f)


def get_settings_value(key, stage='dev'):
    return settings[stage].get(key)


with open(zappa_settings_file, 'r') as f:
    settings = json.load(f)


def get_settings_value(key, stage='dev'):
    return settings[stage].get(key)


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def mkdirs(path):
    dirs = path.split('/')
    mkdir('/'.join(dirs[:-1]))
