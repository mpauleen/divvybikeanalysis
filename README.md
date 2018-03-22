# Divvy Availability Predictor
Analytics Value Chain Project

## Project Charter

Drive fleet management and distribution decisions by anticipating potential shortages and overages at each station in the Divvy network to create a more consistent experience for riders and help them better plan their commutes.

### Vision

Anticipate shortages in the availability of Divvy Bikes at each station around Chicago to help riders and commuters more consistently have access to bikes and bike returns.

### Mission

Drive fleet management and distribution decisions by predicting impending shortages to ensure quick restocking when bikes run out.

### Success Criteria

A web application to visualize bike stations in the Divvy network, and a reliable prediction the probability of a shortage within the next 30 minutes for each station given live data of the station’s status. 
 
## Suggested steps

1. Clone repository

2. Create and activate new virtual environment for dependencies 

    ```bash
    virtualenv -p python3 DivvyBike
    source DivvyBike/bin/activate
    ```

3. Install required packages 

    ```bash
    pip install -r requirements.txt
    ```

4. Sign up for an access token from [Mapbox](https://www.mapbox.com) and set it as the variable `mapToken` in `app/static/map.js`.

5. If desired, select desired training data from the [City of Chicago Data Portal](https://data.cityofchicago.org/dataset/Divvy-Bicycle-Stations-Historical-Dashboard/5nq5-wxpz). Alternatively, data is provided in `develop/data/raw/historical.csv.gz`.

6. Set up divvy.env file specifying the connection string to a Postgre database instance: 

   ```bash
   export CONNSTRING="host=XXX port=XXX user=XXX dbname=XXX password=XXX"
   ```

7. Set your environment

   ```bash
   source divvy.env
   ```

8. Initialize database 

    ```bash
    python create_db.py
    ```
    
9. Clean the environment
    ```bash
    cd develop
    make clean
    ```
10. Prepare features, models, database and geojson and run tests

    ```bash
    make all
    make test
    ```

11. Launch the webapp
    ```bash
    cd ../app
    python app.py
    ```

[Live Demo](http://34.205.16.171:5000/)

[Pivotal Tracker](https://www.pivotaltracker.com/n/projects/2142887)

Project Developer: Michael Pauleen
Project Manager: Arvind Koul
QA: Saurabh Tripathi