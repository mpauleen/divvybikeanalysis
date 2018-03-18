import sys
import os
import numpy as np
import time
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

    api_data = get_two_most_recent(vars['station'])
    features = features_from_api(api_data)
    prediction = round(predict_from_api(
        features.tail(1), vars['station']), 2) * 100

    request_time = time.time()
    station_id = int(vars['station'])
    available = vars['available_bikes']
    docks = vars['docks_in_service']
    percent_full = features['Percent Full'].iloc[0]
    result = prediction
    post_result(request_time, station_id, percent_full, result)

    return render_template("index.html", has_result=True, station_id=vars['station'], docks = docks, available = available, map_lat=vars['lat'],
                           map_long=vars['lng'], map_zoom=vars['zoom'], prediction=prediction, home=False)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
