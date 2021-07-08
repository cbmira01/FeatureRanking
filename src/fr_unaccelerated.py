
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
    return None


def get_distances(dataset):

    max_values = [max(r) for r in [list(x) for x in zip(*dataset)]]
    min_values = [min(r) for r in [list(x) for x in zip(*dataset)]]

    print('\n')
    features = len(dataset[0])
    instances = len(dataset)



    nl = '\n'

    print(nl, 'dataset', dataset)

    diff_ds = [np.subtract(dataset[i], dataset[j]) for i in range(instances-1) for j in range(i+1, instances)]
    print(nl, 'diff_ds', *diff_ds)

    diff_values = [np.subtract(max_values[k], min_values[k]) for k in range(features)]
    print(nl, 'max_values', max_values)
    print(nl, 'min_values', min_values)
    print(nl, 'diff_values', diff_values)

    divs = np.divide(diff_ds, diff_values)
    print(nl, 'divs', divs)

    squares = np.square(divs)
    print(nl, 'squares', squares)

    sum_sq = [np.sum(s) for s in squares]
    print(nl, 'sum_sq', sum_sq)

    distances = np.sqrt(sum_sq)
    print(nl, 'distances', distances)

    average_distance = np.average(distances)
    # print(nl, average_distance)

    alpha = np.divide(-np.log(0.5), average_distance)
    # print(nl, alpha)

    sims = np.exp(np.multiply(-alpha, distances))
    log_sims = np.log10(sims)
    dissims = np.subtract(1, sims)
    log_dissims = np.log10(dissims)

    es = np.add(np.multiply(sims, log_sims), np.multiply(dissims, log_dissims))
    # print(nl, es, sep='\n')

    entropy = - np.sum(es)
    # print(nl, entropy, sep='\n')

if __name__ == '__main__':

    print('\nCheck unaccelerated Feature Ranking on console...\n')

    datasets_list = discover_datasets()
    for ds in datasets_list:
        print(ds['short_name'], '  ', end='')

    ds_name = input('\n\nChose a dataset: ').lower()
    ds_info = next((d for d in datasets_list if d['short_name'] == ds_name), None)

    if ds_info is not None:
        entry(ds_info)
