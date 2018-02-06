from flask import Flask, render_template, request

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
    print vars
#    print station_id, map_long, map_lat, map_zoom
    return render_template("index.html", has_result = True, station_id = vars['station'], map_lat = vars['lat'], map_long = vars['lng'], map_zoom = vars['zoom'])
#, map_long = map_long, map_lat = map_lat, map_zoom = map_zoom
@app.route('/test')
def test():
    return '<h2>Testing</h2>' #you can write html in here!

#now username is a variable if inside "<>"
@app.route('/profile/<username>')
def profile(username):
   return '<h2>Hey there %s<h2>' % username

#for integers you need to specify type int
@app.route('/post/<int:post_id>')
def post(post_id):
   return '<h2>Post ID is %s<h2>' % post_id

#Using HTML Templates
@app.route("/profile2/<name>")
def profile2(name):
    return render_template("profile.html",name=name)

if __name__ == "__main__":
    app.run(debug=True)
