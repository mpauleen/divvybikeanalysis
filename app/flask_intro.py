import sys
import os
import numpy as np
from flask import Flask, render_template, request


sys.path.append(os.path.abspath('../develop/src/'))

from models.predict_model import predict_from_api
from data.access_api import get_two_most_recent
from features.build_features import features_from_api

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", has_result = False, map_lat = 41.881832, map_long = -87.623177, map_zoom = 12, home = True)

@app.route('/get_predict', methods=['GET'])
def predict():
    vars = request.args.to_dict()

    print(vars)
    api_data = get_two_most_recent(vars['station'])
    print(api_data)
    features = features_from_api(api_data)
    print(features)
    prediction = round(predict_from_api(features.tail(1), vars['station']),2)*100
#    print station_id, map_long, map_lat, map_zoom
    return render_template("index.html", has_result = True, station_id = vars['station'], map_lat = vars['lat'], map_long = vars['lng'], map_zoom = vars['zoom'], prediction = prediction, home = False)
#, map_long = map_long, map_lat = map_lat, map_zoom = map_zoom

if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0', port=5643)
