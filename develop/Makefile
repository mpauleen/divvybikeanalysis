../app/static/sites.js:
	python src/data/create_geojson.py

sites:../app/static/sites.js

db:
	python ../create_db.py

data/processed/historical_features.csv:
	python src/features/build_features.py

features:data/processed/historical_features.csv

models/models.pkl:
	python src/models/train_model.py

model:models/models.pkl

clean:
	rm data/processed/historical_features.csv
	rm models/models.pkl
	rm app/static/sites.js

test:
	pytest

all: features model db sites
