import logging
import pandas as pd

from pandas.tseries.holiday import USFederalHolidayCalendar as calendar


def parse_dates(s):
    """
    This is an extremely fast approach to datetime parsing.
    For large data, the same dates are often repeated. Rather than
    re-parse these, we store all unique dates, parse them, and
    use a lookup to convert all dates.
    """
    dates = {date:pd.to_datetime(date) for date in s.unique()}
    return s.map(dates)

def rush_hour_indicator(df):
    """Appends `am_rush` (7 to 11) and `pm_rush` (16 to 19) indicator columns to DF"""
    df['am_rush'] = ((df.ts.dt.hour >= 7) & (df.ts.dt.hour < 11)).astype(int)
    df['pm_rush'] = ((df.ts.dt.hour >= 16) & (df.ts.dt.hour < 19)).astype(int)

def weekend_indicator(df):
    """Appends weekend indicator column"""
    df['weekend'] = (df.ts.dt.weekday >= 5).astype(int)

def holiday_indicator(df):
    """Appends holiday (US Federal) indicator column"""
    min_date = df.ts.min()
    max_date = df.ts.max()
    cal = calendar()
    holidays = cal.holidays(start=min_date, end=max_date)
    df['holiday'] = (df.ts.dt.date.astype('datetime64').isin(holidays)).astype(int)
    
def features_from_csv(df):
    """Generate predictive features from historical csv
    of Divvy Station data. Create holiday, weekend and rush
    hour indicators, as well as shortage indicator (0 bikes available
    at some point within 30 minutes). To be used for training model
    
    Args:
        df (pd.DataFrame): Historical Divvy Data
    
    Returns:
        pd.DataFrame: Features DataFrame for modeling.
    """
    df['ts'] = parse_dates(df.Timestamp)
    holiday_indicator(df)
    weekend_indicator(df)
    rush_hour_indicator(df)
    df['weekend_or_holiday'] = (df['weekend'] | df['holiday']).astype(int)
    df['month'] = df.ts.dt.month
    df['shortage'] = df['Available Bikes'] <= 0
    sorted_df = df.sort_values(by = ['ID','ts'])
    by_id = sorted_df.groupby('ID')

    # Check if shortage occurs in next 30 minutes
    sorted_df['shortage_in_30'] = (by_id.shortage.shift(-1) | by_id.shortage.shift(-2) | by_id.shortage.shift(-3)).astype(int)
    sorted_df['percent_full_lag'] = by_id['Percent Full'].shift(1)
    sorted_df['percent_full_delta'] = sorted_df['percent_full_lag']-sorted_df['Percent Full']
    return sorted_df

def features_from_api(df):
    """Generate predictive features from api pull
    of Divvy Station data. Create holiday, weekend and rush
    hour indicators. To be used for predicting shortage at a station.
    
    Args:
        df (pd.DataFrame): API pull of Divvy Data
    
    Returns:
        pd.DataFrame: Features DataFrame for predicting.
    """
    df['ts'] = parse_dates(df.timestamp)
    holiday_indicator(df)
    weekend_indicator(df)
    rush_hour_indicator(df)
    df['weekend_or_holiday'] = (df['weekend'] | df['holiday']).astype(int)
    df['month'] = df.ts.dt.month
    df['shortage'] = df['available_bikes'] <= 0
    sorted_df = df.sort_values(by = ['ts'])
    by_id = sorted_df.groupby('id')
    sorted_df['shortage_in_30'] = (by_id.shortage.shift(-1) | by_id.shortage.shift(-2) | by_id.shortage.shift(-3)).astype(int)
    sorted_df['percent_full_lag'] = by_id['percent_full'].shift(1)
    sorted_df['percent_full_delta'] = sorted_df['percent_full_lag']-sorted_df['percent_full']
    sorted_df['Percent Full'] = sorted_df['percent_full']
    return sorted_df

def create_feature_df(file_name):
    """Create features from historical station data
    for model training and saves to csv in 
    `data/processed/historical_features.csv`

    Args:
        file_name (str): path to raw csv
    """
    logging.info('Generate features from raw data.')
    hist = pd.read_csv(file_name)
    features = features_from_csv(hist)
    features.to_csv('data/processed/historical_features.csv.gz')
    logging.info('Finished generating features')

if __name__ == "__main__":

    log_fmt = '%(asctime)s -  %(levelname)s - %(message)s'
    logging.basicConfig(filename='create_features.log', level=logging.INFO,
                        format=log_fmt)
    logger = logging.getLogger(__name__)
    create_feature_df('../../data/raw/historical.csv')


