db:
	python ../create_db.py

data/processed/historical_features.csv:
	python src/features/build_features.py

features:data/processed/historical_features.csv

models/params:
	python src/models/train_model.py
model:models/params

clean:
	rm data/processed/historical_features.csv
	rm models/*.pkl

all: features model