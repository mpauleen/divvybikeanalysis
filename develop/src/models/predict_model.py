import pickle
import os
import time
import numpy as np
import statsmodels.api as sm
import pandas as pd
from statsmodels.formula.api import glm

def load_model_params(station_id):
	file_name = "../develop/models/station_{}_params.pkl".format(station_id)
	params = pd.read_pickle	(file_name)
	return params

def log_odds_to_prob(log_odds):
	odds = np.exp(log_odds)
	prob = odds/(1+odds)
	return prob

def log_odds(model_params, df):
	month = df['month'].iloc[0]
	print(df)
	print(model_params)
	print(str(month))
	month_val = 0
	print([str(month) in s for s in model_params.index])
	if int(month) > 1:
		month_val = model_params[[str(month) in s for s in model_params.index]].iloc[0]

	return model_params['Intercept']+month_val+model_params['Q("Percent Full")']*df['Percent Full']\
	+model_params['weekend_or_holiday']*df['weekend_or_holiday']+model_params['am_rush']*df['am_rush']+model_params['pm_rush']*df['pm_rush']\
	+model_params['percent_full_delta']*df['percent_full_delta']

def predict_from_api(df, station_id):
	params = load_model_params(station_id)
	lodds = log_odds(params, df)
	prob = log_odds_to_prob(lodds)
	print(prob)
	return prob.iloc[0]
