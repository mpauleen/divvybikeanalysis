from flask import Flask, render_template, request
import sys
import os
sys.path.append(os.path.abspath('../develop/models'))
from predict import predict_shortage

app = Flask(__name__)

#here we are routing/mapping using decorator '@' -- use it to map URL to return value
#the response to the URL is what the function returns
# @ signifies a decorator
@app.route('/')
def index():
    return render_template("index.html", has_result = False, map_lat = 41.881832, map_long = -87.623177, map_zoom = 12)
@app.route('/get_predict', methods=['GET'])

def predict():
#    station_id = request.form['id']
    vars = request.args.to_dict()
    prediction = round(predict_shortage(vars['station']),2)*100
    print vars
#    print station_id, map_long, map_lat, map_zoom
    return render_template("index.html", has_result = True, station_id = vars['station'], map_lat = vars['lat'], map_long = vars['lng'], map_zoom = vars['zoom'], prediction = prediction)
#, map_long = map_long, map_lat = map_lat, map_zoom = map_zoom

if __name__ == "__main__":
    app.run(debug=True)
