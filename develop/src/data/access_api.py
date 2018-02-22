import sodapy
import pandas as pd
import datetime


client = sodapy.Socrata("data.cityofchicago.org", None)

def pull_data(id):
	today = datetime.datetime.now()
	datestring = (today-datetime.timedelta(days = 1)).strftime("%Y-%m-%dT%H:%M:%S")
	results = client.get("eq45-8inv", id = id, limit = 2000)
	results_df = pd.DataFrame.from_records(results)
	return results_df