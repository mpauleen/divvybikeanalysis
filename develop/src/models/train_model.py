import sys
import os
import pickle
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import glm



sys.path.append(os.path.abspath('../../'))
from src.features.build_features import features_from_csv

def create_feature_df(file_name):
    hist = pd.read_csv(file_name)
    features = features_from_csv(hist)
    features.to_csv('../../data/processed/historical_features.csv')
    return features

def train_models(df):
    unique_ids = df.ID.unique()
    station_models = dict.fromkeys(unique_ids)
    for station_id in unique_ids:
        print(station_id)
        model = glm('shortage_in_30 ~ C(month)+Q("Percent Full")+weekend_or_holiday+am_rush+pm_rush+percent_full_delta', data=df[df.ID == station_id], family=sm.families.Binomial())
        fitted_model = model.fit()
        
        fitted_model.params.to_pickle('../../models/station_{}_params.pkl'.format(station_id))
        # fname = "../../models/station_{}.pkl".format(station_id)
        # fitted_model.save(fname, remove_data=True)
if __name__ == "__main__":
    train_models(pd.read_csv('../../data/processed/historical_features.csv'))
