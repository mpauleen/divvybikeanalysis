import sodapy
import pandas as pd
import datetime



def get_two_most_recent(id):
	client = sodapy.Socrata("data.cityofchicago.org", None)
	results = client.get("eq45-8inv", id = id, limit = 2)
	results_df = pd.DataFrame.from_records(results)
	results_df[['id', 'percent_full','available_bikes']] = results_df[['id', 'percent_full','available_bikes']].apply(pd.to_numeric, errors='coerce')
	return results_df