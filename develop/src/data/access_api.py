import sodapy
import pandas as pd
import datetime


def get_two_most_recent(id):
    """Query the Divvy API for the two most recent tuples
    of the specified station for prediction

    
    Args:
        id (int): Station ID in Divvy network
    
    Returns:
        pd.DataFrame: DF containing data pulled from API
    """
    client = sodapy.Socrata("data.cityofchicago.org", None)
    results = client.get("eq45-8inv", id=id, limit=2)
    results_df = pd.DataFrame.from_records(results)

    # convert numeric columns to numeric
    results_df[['id', 'percent_full', 'available_bikes']] = results_df[
        ['id', 'percent_full', 'available_bikes']].apply(pd.to_numeric, errors='coerce')
    return results_df