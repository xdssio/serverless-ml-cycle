import os

import boto3

import config
from ml.model import Model

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
    test_name = 'test-model-state'
    model = Model()
    model.fit(save=False)
    path = model.save(model_name=test_name, upload=False)
    model = Model.load(model_path=path)
    assert len(model.predict(data.head(10))) > 0
    os.remove(path)


def test_upload_and_download():
    test_name = 'test-model'
    session = boto3.Session()
    s3 = session.resource('s3')
    obj = s3.Object(config.models_bucket, test_name)
    obj.delete()

    model = Model()
    model.fit(save=False)
    path = model.save(test_name, upload=False)
    model.upload(test_name, model_path=path)

    path = Model.download(model_name=test_name)
    model = Model.load(model_path=path)
    predictions = model.predict(data.head(10))
    assert len(predictions) == 10
    assert 1 in predictions
    assert 0 in predictions

    obj = s3.Object(config.models_bucket, test_name)
    obj.delete()

    model = Model()
    model.fit(save=False)
    model.save(model_name=test_name)
    model = Model.load(model_name=test_name)
    assert len(model.predict(data.head(10))) > 0


def train_model():
    model = Model()
    model.fit(save=True, upload=True)
