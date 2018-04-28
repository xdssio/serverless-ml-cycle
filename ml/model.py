import datetime as dt
import io
import os

import boto3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from ml.pipeline import create_pipeline
from ml.utils import get_settings_value


class Model():
    def __init__(self):
        self.created = dt.datetime.now()
        self.updated = self.created
        self.version = -1
        self.pipeline = create_pipeline()
        self.estimator = RandomForestClassifier()
        self.pipeline.steps.append(('estimator', self.estimator))
        self.features = get_settings_value('model_features')
        self.target = get_settings_value('model_target')
        self.model_name = get_settings_value('model_name')

    def increment(self):
        self.version += 1

    def fit(self, data=None, save=True):
        data = data if data is not None else self.get_data()
        data = self.preprocess(data)
        self.pipeline.fit(X=data[self.features], y=data[self.target])
        self.increment()
        if save:
            self.save()

    def predict(self, X):
        return self.pipeline.predict(X)

    def innovations(self):
        """
        When you want to run on a csv
        """
        pass

    def health(self):
        return self.pipeline is not None

    def preprocess(self, data):
        data['Sex'] = data['Sex'].astype('bool')
        data['Pclass'] = data['Pclass'].astype('category')
        return data.dropna()

    @staticmethod
    def get_data(from_date=None, to_date=None):
        """
        In the future, you miight want to get only new data
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

    def save(self, model_name=None, bucket=None):
        s3 = boto3.client('s3')
        model_key = model_name if model_name else get_settings_value('model_name')
        bucket = bucket if bucket else get_settings_value('models_bucket')
        model_path = '/'.join(['./tmp', model_key])
        os.makedirs('./tmp', exist_ok=True)
        joblib.dump(self, model_path)
        resp = s3.put_object(Body=open(model_path, 'rb'), Bucket=bucket, Key=model_key)
        return resp

    @staticmethod
    def load(model_name=None, bucket=None):
        s3 = boto3.client('s3')
        model_key = model_name if model_name else get_settings_value('model_name')
        bucket = bucket if bucket else get_settings_value('models_bucket')
        obj_string = s3.get_object(Bucket=bucket, Key=model_key)['Body'].read()
        model_path = '/'.join(['./tmp', model_key])
        with open(model_path, "wb") as the_file:
            the_file.write(obj_string)
        model = joblib.load(model_path)
        return model
