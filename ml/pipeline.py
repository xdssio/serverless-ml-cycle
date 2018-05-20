import sklearn.preprocessing as pp
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn_pandas import CategoricalImputer
from sklearn_pandas import DataFrameMapper

target = 'Survived'
mapper = DataFrameMapper([
    (['Age', 'Fare', 'SibSp'], pp.Imputer()),
    (['Embarked'], [CategoricalImputer(), pp.LabelEncoder(), pp.LabelBinarizer()]),
    (['Age', 'Fare'], pp.StandardScaler()),
], default=False)


def create_pipeline():
    return Pipeline([
        ('process', mapper),
        ('estimator', RandomForestClassifier())
    ])
