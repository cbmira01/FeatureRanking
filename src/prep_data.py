
#
# Dataset operations
#

import numpy as np
import csv
import pprint
import json


def discover_datasets():
    with open('../data/datasets.json', 'r') as file:
        datasets_dict = json.load(file)
    return datasets_dict['datasets']


def clean_data(dataset_info):
    # retrieve data
    # drop rows
    # drop columns
    # convert to float
    return dataset


def drop_rows(dataset_csv, rows):
    return dataset_csv


def drop_columns(dataset_csv, cols):
    return dataset_csv


def convert_to_float(dataset_csv):
    return dataset


def dump_dataset_to_console(dataset):
    return None


num_rows = 12
drop_rows = [10, 11]
num_columns = 8
drop_columns = [5, 6, 7]

with open('../data/example/data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # dataset = list(reader)
    dataset_str = []
    for row in reader:
        dataset_str.append(row[:])

pp = pprint.PrettyPrinter(width=100, compact=True)

pp.pprint(dataset_str)
print('\n')

dataset = [[float(col) for col in row] for row in dataset_str]
pp.pprint(dataset)

# ---------------------------------
