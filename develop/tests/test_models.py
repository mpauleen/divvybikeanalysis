import pickle
import pandas as pd
import pytest

from src.features import build_features
from src.models import predict_model

# load model file
with open('models/models.pkl', 'rb') as handle:
    models = pickle.load(handle)

# create test data
data = pd.DataFrame.from_records([{'address': 'Buckingham Fountain', 'available_bikes': '3', 'available_docks': '24', 'docks_in_service': '27', 'id': '2', 'latitude': '41.876393', 'location': {'type': 'Point', 'coordinates': [-87.620328, 41.876393]}, 'longitude': '-87.620328', 'percent_full': '11', 'record': '220180318133545', 'station_name': 'Buckingham Fountain', 'status': 'In Service', 'timestamp': '2018-03-18T13:35:45.000', 'total_docks': '27'}, {
                                 'address': 'Buckingham Fountain', 'available_bikes': '4', 'available_docks': '23', 'docks_in_service': '27', 'id': '2', 'latitude': '41.876393', 'location': {'type': 'Point', 'coordinates': [-87.620328, 41.876393]}, 'longitude': '-87.620328', 'percent_full': '15', 'record': '220180318132539', 'station_name': 'Buckingham Fountain', 'status': 'In Service', 'timestamp': '2018-03-18T13:25:39.000', 'total_docks': '27'}])

data[['id', 'percent_full', 'available_bikes']] = data[
    ['id', 'percent_full', 'available_bikes']].apply(pd.to_numeric, errors='coerce')


def test_model_params_exist():
    """Ensure model parameters are properly formed"""
    expected_index = set(['Intercept', 'C(month)[T.2]', 'C(month)[T.3]',
                          'C(month)[T.4]', 'C(month)[T.5]', 'C(month)[T.6]',
                          'C(month)[T.7]', 'C(month)[T.8]',
                          'C(month)[T.9]', 'C(month)[T.10]',
                          'C(month)[T.11]', 'C(month)[T.12]', 'Q("Percent Full")',
                          'weekend_or_holiday', 'am_rush',
                          'pm_rush', 'percent_full_delta'])
    for station_id, model in models.items():
        assert set(model.index) == expected_index


def test_build_features():
    """Check feature construction"""
    feat = build_features.features_from_api(data)
    assert feat.shape == (2,26)

def test_predictions():
    """Check that prediction is between 0 and 1"""
    feat = build_features.features_from_api(data)
    station_id = feat['id'].iloc[0]
    prediction = predict_model.predict_from_api(models, feat, station_id)
    assert (0 <= prediction) & (prediction <= 1)