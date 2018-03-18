import sys
import os
import numpy as np
import time
from datetime import datetime
from flask import Flask, render_template, request

sys.path.append(os.path.abspath('../'))
from create_db import post_result

sys.path.append(os.path.abspath('../develop/src/'))

from models.predict_model import predict_from_api
from data.access_api import get_two_most_recent
from features.build_features import features_from_api

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", has_result=False, map_lat=41.881832,
                           map_long=-87.623177, map_zoom=12, home=True)


@app.route('/get_predict', methods=['GET'])
def predict():
    vars = request.args.to_dict()
    print(vars)
    api_data = get_two_most_recent(vars['station'])
    features = features_from_api(api_data)
    prediction = round(predict_from_api(
        features.tail(1), vars['station']), 2) * 100

    request_time = time.time()
    update_dt = datetime.strptime(features['timestamp'].iloc[1], '%Y-%m-%dT%H:%M:%S.000')
    update_date = datetime.strftime(update_dt, '%d/%m/%Y')
	update_time = datetime.strftime(update_dt, '%H:%M')
    station_id = int(vars['station'])
    available = features['available_bikes'].iloc[1]
    docks = features['docks_in_service'].iloc[1]
    percent_full = features['Percent Full'].iloc[1]
    result = prediction
    post_result(request_time, station_id, percent_full, result)

    return render_template("index.html", has_result=True, station_id=vars['station'],
                           update_date = update_date, update_time = update_time, docks = docks,
                           available = available, map_lat=vars['lat'],
                           map_long=vars['lng'], map_zoom=vars['zoom'],
                           prediction=prediction, home=False)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)



