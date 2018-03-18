../app/static/sites.js:
	python src/data/create_geojson.py
sites:../app/static/sites.js

db:
	python ../create_db.py

data/processed/historical_features.csv:
	python src/features/build_features.py

features:data/processed/historical_features.csv

models/params.txt:
	@touch models/params.txt; python src/models/train_model.py

model:models/params.txt

clean:
	rm data/processed/historical_features.csv
	rm models/*
	rm app/static/sites.js
all: features model db sites
