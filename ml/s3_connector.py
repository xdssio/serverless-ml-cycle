import os

import boto3

from ml.utils import get_settings_value, mkdir, mkdirs

s3_connection = boto3.client('s3')
model_bucket = s3_connection.get_bucket(get_settings_value('model_bucket'))
dataset_bucket = s3_connection.get_bucket(get_settings_value('dataset_bucket'))


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
