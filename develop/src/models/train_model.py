import sys
import os
import pickle
import logging
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import glm


sys.path.append(os.path.abspath('../../'))
sys.path.append(os.path.abspath('.'))
from src.features.build_features import features_from_csv



def train_models(df):
    """Take in feature data frame and train a logit
    model for each station in the Divvy network. Save
    model coefficients to `data/models`

    Args:
        df (pd.DataFrame): features data frame
    """
    unique_ids = df.ID.unique()
    station_models = dict.fromkeys(unique_ids)
    for station_id in unique_ids:
        logging.info('Training model for station {}.'.format(station_id))
        model = glm('shortage_in_30 ~ C(month)+Q("Percent Full")+weekend_or_holiday+am_rush+pm_rush+percent_full_delta',
                    data=df[df.ID == station_id], family=sm.families.Binomial())
        fitted_model = model.fit()
        station_models[station_id] = fitted_model.params
    logging.info('Pickling models')
    with open('models/models.pkl', 'wb') as handle:
        pickle.dump(station_models, handle)


if __name__ == "__main__":

    log_fmt = '%(asctime)s -  %(levelname)s - %(message)s'
    logging.basicConfig(filename='train_models.log', level=logging.INFO,
                        format=log_fmt)
    logger = logging.getLogger(__name__)

    logging.info('loading features from csv')
    features = pd.read_csv('data/processed/historical_features.csv')
    train_models(features)
