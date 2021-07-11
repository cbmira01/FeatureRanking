
#
# This is the unaccelerated Feature Ranking implementation
#

import numpy as np
import sys
from prep_data import *


def entry(dataset_info):
    print(dataset_info)
    dataset = get_clean_data(dataset_info, dump=False)

    get_entropy(dataset)
    return None


def get_entropy(dataset):

    features = len(dataset[0])
    instances = len(dataset)

    max_values = [max(r) for r in [list(d) for d in zip(*dataset)]]
    min_values = [min(r) for r in [list(d) for d in zip(*dataset)]]

    sample_differences = [
    np.subtract(dataset[i], dataset[j])
    for i in range(instances-1)
    for j in range(i+1, instances)
    ]

    value_ranges = [
    np.subtract(max_values[k], min_values[k])
    for k in range(features)
    ]

    squares = np.square(np.divide(sample_differences, value_ranges))
    sample_distances = np.sqrt([np.sum(s) for s in squares])

    average_distance = np.average(sample_distances)
    alpha = np.divide(-np.log(0.5), average_distance)

    sims = np.exp(np.multiply(-alpha, sample_distances))
    sims = [i for i in sims if i not in [1.0]]
    dissims = np.subtract(1, sims)

    entropy_pairwise = np.add(np.multiply(sims, np.log10(sims)), np.multiply(dissims, np.log10(dissims)))
    entropy_total = - np.sum(entropy_pairwise)

    return None


if __name__ == '__main__':

    print('\nCheck unaccelerated Feature Ranking on console...\n')

    datasets_list = discover_datasets()
    for ds in datasets_list:
        print(ds['short_name'], '  ', end='')

    ds_name = input('\n\nChose a dataset: ').lower()
    ds_info = next((d for d in datasets_list if d['short_name'] == ds_name), None)

    if ds_info is not None:
        entry(ds_info)
