import boto3

from ml.model import Model
from ml.utils import get_settings_value


def test_get_data():
    model = Model()
    df = model.get_data()
    assert len(df) > 0


def test_train():
    model = Model()
    assert model.version == -1
    model.fit()
    assert model.version == 0


def test_save_and_load():
    test_name = 'test-model'
    s3 = boto3.resource('s3')
    obj = s3.Object(get_settings_value('models_bucket'), test_name)
    obj.delete()

    model = Model()
    model.fit(save=False)
    model.save(test_name)
    self = Model.load(test_name)
    df = model.get_data()
    predictions = self.predict(df.head(10))
    assert len(predictions) == 10
    assert 1 in predictions
    assert 0 in predictions

