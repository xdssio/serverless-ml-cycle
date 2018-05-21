import os

models_bucket = "serverless-ml-models"
data_bucket = "xdss-public-datasets"
data_key = "kaggle/titanic_data.csv"
model_name = "titanic-model"
tmp_folder = os.environ.get('TMP_FOLDER', "./tmp")
model_key_name = "model.pkl"
model_target = "Survived"
model_features = [
    "Fare",
    "Age",
    "Pclass",
    "SibSp",
    "Embarked",
    "Sex"
]
