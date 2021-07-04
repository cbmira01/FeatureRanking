
import json

# Discover all the available datasets
with open('../data/datasets.json', 'r') as f:
    datasets = json.load(f)

for d in datasets['datasets']:
    print(d['short_name'], d['long_name'])


# Main command loop
# - List datasets
# - Run feature reduction on a dataset
