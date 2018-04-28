import os

import boto3

from ml.utils import get_settings_value, mkdir, mkdirs, get_function_name

s3_connection = boto3.client('s3')
lambda_client = boto3.client('lambda')


def download_dir_s3(bucket, local_folder):
    mkdir(local_folder)
    for key in bucket.list():
        if str(key.name).startswith(local_folder):
            mkdirs(key.name)
            if not key.name.endswith('/'):
                try:
                    res = key.get_contents_to_filename('./' + key.name)
                except OSError as e:
                    print(e)


def upload_to_s3(bucketname, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            s3_connection.upload_file(file_path, bucketname, file_path)


def update_function_version(version=None, function_name=None):
    if function_name is None:
        function_name = get_function_name()
    if version is None or not str(version).isdigit():
        return None
    environemnt = {'Variables': {
        'VERSION': str(version)
    }
    }
    response = lambda_client.update_function_configuration(function_name, Environment=environemnt)
    return response


def list_model_version(model_name=None):
    model_name = model_name if model_name else get_settings_value('model_name')
    bucket = get_settings_value('models_bucket')
    ret = []
    for key in s3_connection.list_objects(Bucket=bucket)['Contents']:
        s3_path = key.get('Key')
        if s3_path.endswith(model_name):
            version = s3_path.split('/')[0]
            print(version, version.isdigit())
            if version.isdigit():
                ret.append(int(version))
    return ret


def get_highest_version(model_name=None):
    versions = list_model_version(model_name=model_name)
    return max(versions)
