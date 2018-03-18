import json
import logging
import pandas as pd


def df_to_geojson(df, properties, lat='Latitude', lon='Longitude'):
    """Extract divvy bike site locations from df and convert"""
    logging.info('create sites')
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson
	
def main():
    """Create sites.js in static folder"""
    log_fmt = '%(asctime)s -  %(levelname)s - %(message)s'
    logging.basicConfig(filename='create_geojson.log', level=logging.INFO,
                        format=log_fmt)
    logger = logging.getLogger(__name__)
    divvy = pd.read_csv('data/raw/historical.csv.gz')
    locations = divvy[['ID','Latitude','Longitude','Station Name','Address']].drop_duplicates('ID').sort_values('ID')
    geo_json = df_to_geojson(locations, ['ID','Station Name','Address'])
    output_filename = '../app/static/sites.js'
    with open(output_filename, 'w') as output_file:
        output_file.write('var sites = ')
        json.dump(geo_json, output_file, indent=2)
    
if __name__ == "__main__": 
    main()