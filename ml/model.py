import io

import boto3
import datetime.datetime as dt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from ml.pipeline import pipeline
from ml.utils import get_settings_value


class Model():
    def __init__(self):
        self.created = dt.now()
        self.updated = self.created
        self.version = -1
        self.pipeline = pipeline
        self.pipeline.steps.append(['estimator', RandomForestClassifier()])
        self.features = get_settings_value('model_features')
        self.target = get_settings_value('model_target')

    def increment(self):
        self.version += 1

    def train(self):
        df = self.get_data()
        self.pipeline.fit(X=df[self.features], y=self.target)
        self.increment()
        self.save()

    def predict(self, X):
        return self.pipeline.predict(X)

    def innovations(self):
        pass

    def health(self):
        return self.pipeline is not None

    def preprocess(self):
        pass

    def get_data(self, from_date=None, to_date=None):
        """
        In the future, you miight want to get only new data
        :param from_date:
        :param to_date:
        :return:
        """
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket='xdss-public-datasets', Key='kaggle/titanic_data.csv')
        return pd.read_csv(io.BytesIO(obj['Body'].read()))

    def save(self):
        pass

    def upload(self):
        pass

    @staticmethod
    def download(self):
        pass
