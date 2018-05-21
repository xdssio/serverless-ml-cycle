import datetime as dt
import io
import pathlib

import boto3
import pandas as pd
from sklearn.externals import joblib

from ml.pipeline import create_pipeline
from ml.utils import get_settings_value


class Model:
    def __init__(self, model_name=None):
        self.created = dt.datetime.now()
        self.updated = self.created
        self.version = -1
        self.pipeline = create_pipeline()
        self.features = get_settings_value('model_features')
        self.target = get_settings_value('model_target')
        self.model_name = model_name if model_name else get_settings_value('model_name')

    def increment(self):
        self.version += 1

    def preprocess(self, data):
        # We don't really need this, but for possible use cases
        data['Sex'] = data['Sex'].astype('bool')
        data['Pclass'] = data['Pclass'].astype('category')
        return data.dropna()

    def fit(self, data=None, save=True, upload=True, path=None,):
        data = data if data is not None else self.get_data()
        data = self.preprocess(data)
        self.pipeline.fit(X=data[self.features], y=data[self.target])
        self.increment()
        if save:
            self.save(model_name=self.model_name, path=path, upload=upload)

    def get_version(self):
        return self.version

    def predict(self, X):
        return self.pipeline.predict(X)

    def innovations(self):
        """
        When you want to run on a csv or fit to the Sagemaker API
        """
        pass

    def health(self):
        return self.pipeline is not None

    @staticmethod
    def get_data(from_date=None, to_date=None):
        """
        In the future, you might want to get only new data
        :param from_date:
        :param to_date:
        :return:
        """
        s3 = boto3.client('s3')
        bucket = get_settings_value('data_bucket')
        key = get_settings_value('data_key')
        obj = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(io.BytesIO(obj['Body'].read()))
        return df

    def save(self, model_name=None, path=None, upload=True):
        model_key_name = model_name if model_name else get_settings_value('model_key_name')
        model_version = str(self.version)
        model_tmp_folder = get_settings_value('tmp_folder')
        model_location = path if path is not None else '/'.join([model_tmp_folder, model_name, model_version])
        pathlib.Path(model_location).mkdir(parents=True, exist_ok=True)
        model_path = '/'.join([model_location, model_key_name])
        joblib.dump(self, model_path)
        if upload:
            self.upload(model_name=model_key_name, model_path=model_path)
        return model_path

    def upload(self, model_name=None, model_path=None, bucket=None):
        s3 = boto3.client('s3')
        bucket = bucket if bucket else get_settings_value('models_bucket')
        model_name = model_name if model_name else get_settings_value('model_name')
        model_key = self.get_model_key(model_name=model_name)
        resp = s3.put_object(Body=open(model_path, 'rb'), Bucket=bucket, Key=model_key)
        return resp

    @staticmethod
    def download(model_name=None, version=0, model_path=None, bucket=None):
        s3 = boto3.client('s3')
        model_name = model_name if model_name else get_settings_value('model_name')
        model_key_name = get_settings_value('model_key_name')
        model_key = '/'.join([model_name, str(version), model_key_name])
        bucket = bucket if bucket else get_settings_value('models_bucket')
        try:
            obj_string = s3.get_object(Bucket=bucket, Key=model_key)['Body'].read()
        except:
            raise ValueError('Model name or version are bad')

        if model_path is None:
            tmp_folder = get_settings_value('tmp_folder')
            model_path = '/'.join([tmp_folder, model_key])

        with open(model_path, "wb") as the_file:
            the_file.write(obj_string)
        print('model_path: %s' % model_path)
        return model_path

    @staticmethod
    def load(model_path=None, model_name=None, version=0, bucket=None):
        if model_path is None:
            model_path = Model.download(model_name=model_name, version=version, bucket=bucket)
        model = joblib.load(model_path)
        return model

    def get_model_key(self, model_name=None, version=None):
        version = version if version is not None else self.version
        model_key_name = get_settings_value('model_key_name')
        model_name = model_name if model_name else get_settings_value('model_name')
        return '/'.join([model_name, str(version), model_key_name])

    def get_estimator(self):
        return self.pipeline.steps[-1][1]
