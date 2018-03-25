import os

import boto3

from ml.utils import get_settings_value, mkdir, mkdirs,get_function_name

s3_connection = boto3.client('s3')
model_bucket = s3_connection.get_bucket(get_settings_value('model_bucket'))
dataset_bucket = s3_connection.get_bucket(get_settings_value('dataset_bucket'))
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



def update_function_dersion(version=None, function_name=None):
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
