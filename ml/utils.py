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


def get_environment_variable(key):
    return os.environ.get(key, None)


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def mkdirs(path):
    dirs = path.split('/')
    mkdir('/'.join(dirs[:-1]))


def get_pipeline():
    # TODO
    return None


def get_function_name():
    stage = get_environment_variable('STAGE')
    project_name = get_settings_value('project_name', stage)
    return "-".join([get_environment_variable(project_name, stage)])
