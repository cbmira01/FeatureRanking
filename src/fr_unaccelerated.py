
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
    
    # 
    
    return None
    

def ranking_protocol(dataset_info):
    print(dataset_info)
    dataset = get_clean_data(dataset_info, dump=False)
    # need column names (get this in prep_data)
    # dataset needs column labels

    # Step 1: Start with an initial full set of features (no exclusions).
    # exclude = [width of features, all elements False]
    
    while True:
        # Step 2: Find the total entropy of the remaing dataset.
        # dataset = masked(dataset, exlude)
        # total_entropy = get_dataset_entropy(dataset)
        
        # Step 3: Find the feature entropy of each non-excluded feature.
        # feature_entropies = get_feature_entropies(dataset)
    
        # Step 4: Find the feature fk such that the difference between the
        #   total entropy and feature entropy for fk is minimum.
        # entropy_difference = min(np.abs(np.subtract(total_entropy, feature_entropies)))
        #       need feature index
    
        # Step 5: Exclude feature fk from the dataset and record it as the 
        #   "least contributing" feature. 
        # exclude[fk] = True
        # print(column name of fk)
    
        # Step 6: Repeat steps 2–4 until there is only one feature in F.
        # if (there is only one unexcluded feature in exclude):
        break

    # Step 7: Report the last remaining feature is the "most contributing" feature.
    # print(that last remaining fk)
    
    return None
    
    
    
def get_dataset_entropy(dataset):

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

    return entropy_total
    
    
def get_feature_entropies():

    features = len(dataset[0])
    instances = len(dataset)

    # figure out if some of these calculations can be memoized

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

    # figure out how to do column-wise entropies

    return feature_entropies


if __name__ == '__main__':

    print('\nCheck unaccelerated Feature Ranking on console...\n')

    datasets_list = discover_datasets()
    for ds in datasets_list:
        print(ds['short_name'], '  ', end='')

    ds_name = input('\n\nChose a dataset: ').lower()
    ds_info = next((d for d in datasets_list if d['short_name'] == ds_name), None)

    if ds_info is not None:
        entry(ds_info)
