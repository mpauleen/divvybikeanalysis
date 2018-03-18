import pickle
import os
import time
import numpy as np
import statsmodels.api as sm
import pandas as pd
from statsmodels.formula.api import glm


def load_model_params(station_id):
    """Unpickles the stored model coefficients for the specified station_id

    Args:
        station_id (int): Valid Station ID number in the divvy network

    Returns:
        pd.DataFrame: Logit Model Parameters
    """
    file_name = "../develop/models/station_{}_params.pkl".format(station_id)
    params = pd.read_pickle(file_name)
    return params


def log_odds_to_prob(log_odds):
    """Convert log_odds to a probability

    Args:
        log_odds (float): Log odds

    Returns:
        float: probability [0,1]
    """
    odds = np.exp(log_odds)
    prob = odds / (1 + odds)
    return prob


def log_odds(model_params, df):
    """Multiply model parameters and features and calculat log-odds
    the station having 0 bikes available at some point in the next
    30 minutes.

    Args:
        model_params (pd.DataFrame): Logit Model Coefficients
        df (pd.DataFrame): Predictor values

    Returns:
        float: log-odds of bike shortage
    """
    month = df['month'].iloc[0]
    month_val = 0

    # base level for month is 1, so calculate values if not 1
    if int(month) > 1:
        month_val = model_params[
            [str(month) in s for s in model_params.index]].iloc[0]

    return model_params['Intercept'] + month_val + model_params['Q("Percent Full")'] * df['Percent Full']\
        + model_params['weekend_or_holiday'] * df['weekend_or_holiday'] \
        + model_params['am_rush'] * df['am_rush'] + model_params['pm_rush'] * df['pm_rush']\
        + model_params['percent_full_delta'] * df['percent_full_delta']


def predict_from_api(models, df, station_id):
    """Predict probability of shortage of bikes at given station
    in the next 30 minutes given a df of predictors.

    Args:
        df (pd.DataFrame): predictor values, pulled from api
        station_id (int): Divvy Station ID

    Returns:
        float: Probability of shortage
    """
    params = models[station_id]
    lodds = log_odds(params, df)
    prob = log_odds_to_prob(lodds)
    return prob.iloc[0]
