import boto3
import pandas as pd

from ml.model import Model
from ml.utils import get_settings_value

data = Model.get_data()


def test_get_estimator():
    model = Model()
    estimator = model.get_estimator()
    assert estimator is not None


def test_get_data():
    model = Model()
    df = model.get_data()
    assert len(df) > 0


def test_train():
    model = Model()
    assert model.version == -1
    model.fit(save=False)
    assert model.version == 0
    model.predict(data.head(10))


def test_save_and_load():
    test_name = 'test-model'
    session = boto3.Session()
    s3 = session.resource('s3')
    obj = s3.Object(get_settings_value('models_bucket'), test_name)
    obj.delete()

    model = Model()
    model.fit(save=False)
    model.save(test_name)
    model = Model.load(test_name)
    predictions = model.predict(data.head(10))
    assert len(predictions) == 10
    assert 1 in predictions
    assert 0 in predictions


def test_app():
    pd.read_json(data.head(1).to_json())
