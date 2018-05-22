import json
import logging
import os

import boto3

import config

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

zappa_settings_file = 'zappa_settings.json'

with open(zappa_settings_file, 'r') as f:
    settings = json.load(f)

with open(zappa_settings_file, 'r') as f:
    settings = json.load(f)


def get_settings_value(key, stage='dev'):
    return str(settings[stage].get(key))


def list_model_versions(model_name=None):
    s3_connection = boto3.client('s3')
    model_name = model_name if model_name else config.model_name
    bucket = config.models_bucket
    ret = []
    for key in s3_connection.list_objects(Bucket=bucket)['Contents']:
        s3_path = key.get('Key')
        if s3_path.startswith(model_name):
            version = s3_path.split('/')[1]
            if version.isdigit():
                ret.append(int(version))
    return ret


def get_version(model_name):
    version = os.environ.get('VERSION')
    if version is None:
        version = get_highest_version(model_name=model_name)
    return version


def get_highest_version(model_name=None):
    versions = list_model_versions(model_name=model_name)
    return max(versions)


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
