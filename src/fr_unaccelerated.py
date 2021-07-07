
#
# This is the unaccelerated Feature Ranking implementation
#

import numpy as np
import sys
from prep_data import *


def entry(dataset_info):
    print(dataset_info)
    dataset = get_clean_data(dataset_info, dump=False)



    distances = get_distances(dataset)
    print('distances', distances)
    return None


def get_distances(dataset):

    max_values = [max(r) for r in [list(x) for x in zip(*dataset)]]
    min_values = [min(r) for r in [list(x) for x in zip(*dataset)]]
    print('max', max_values)
    print('min', min_values)


    print('\n')
    features = len(dataset[0])
    instances = len(dataset)

    distances = [[[] for _ in range(instances)] for _ in range(instances)]
    print(distances)

    for i in range(instances-1):
        for j in range(i+1, instances):
            d = 0
            for k in range(features):
                d = d + np.square((dataset[i][k] - dataset[j][k]) / (max_values[k] - min_values[k]))
            distances[i][j] = np.sqrt(d)
    print(distances)


if __name__ == '__main__':

    print('\nCheck unaccelerated Feature Ranking on console...\n')

    datasets_list = discover_datasets()
    for ds in datasets_list:
        print(ds['short_name'], '  ', end='')

    ds_name = input('\n\nChose a dataset: ').lower()
    ds_info = next((d for d in datasets_list if d['short_name'] == ds_name), None)

    if ds_info is not None:
        entry(ds_info)
