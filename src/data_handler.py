
#
# Dataset operations
#

import csv
import json
import sys


def discover_datasets():
    with open('../data/datasets.json', 'r') as file:
        datasets_dict = json.load(file)
    return datasets_dict['datasets']


def get_label_names(dataset_info):
    short_name = dataset_info['short_name']
    drop_attributes = dataset_info['remove_attributes']

    with open('../data/' + short_name + '/names.json', 'r') as file:
        label_names = json.load(file)

    for i in sort_and_zero_base(drop_attributes):
        del(label_names[i])

    return label_names


def get_clean_data(dataset_info, dump=False):
    dataset_csv = get_raw_data(dataset_info)

    dataset_csv = drop_rows_and_columns(
        dataset_csv,
        dataset_info['remove_instances'],
        dataset_info['remove_attributes'])

    dataset = [[float(col) for col in row] for row in dataset_csv]

    if (dump):
        dump_dataset(dataset)

    return dataset


def get_raw_data(dataset_info, dump=False):
    short_name = dataset_info['short_name']

    with open('../data/' + short_name + '/data.csv', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        dataset_csv = []
        for row in reader:
            dataset_csv.append(row[:])

    if (dump):
        dump_dataset(dataset_csv)

    return dataset_csv


def drop_rows_and_columns(dataset_csv, rows, cols):
    for row in sort_and_zero_base(rows):
        del(dataset_csv[row])

    for col in sort_and_zero_base(cols):
        for row in range(0, len(dataset_csv)):
            del(dataset_csv[row][col])

    return dataset_csv


def sort_and_zero_base(list):
    list.sort(reverse=True)
    return [x-1 for x in list]


def dump_dataset(dataset):
    print('\n')

    for row in range(0, len(dataset)):
        print(dataset[row])

    return None


if __name__ == '__main__':

    print('\nCheck datasets on console...\n')

    datasets_list = discover_datasets()
    for ds in datasets_list:
        print(ds['short_name'], '  ', end='')

    ds_name = input('\n\nDump a dataset: ').lower()
    ds_info = next((d for d in datasets_list if d['short_name'] == ds_name), None)

    if ds_info is not None:
        dataset_csv = get_raw_data(ds_info, dump=True)
        dataset = get_clean_data(ds_info, dump=True)
