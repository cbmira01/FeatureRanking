
#
# This is the unaccelerated Feature Ranking implementation
#

import numpy as np
import sys
from prep_data import *


def ranking_protocol(dataset_info):
    # print(dataset_info)
    dataset = get_clean_data(dataset_info, dump=False)
    # need column names (get this in prep_data)
    # dataset needs column labels

    # Step 1: Start with an initial full set of features (no exclusions).
    exclude = [False for i in range(len(dataset[0]))]

    while True:
        print('\n exclude: ', exclude)
        # sys.exit('\n\nstopped')

        # Step 2: Find the total entropy of the remaing dataset, and the
        #   feature entropies of each non-excluded feature.
        dataset = [dataset[k] for k in range(len(exclude)) if exclude[k] == False]

        print('\n dataset: ', dataset)
        # sys.exit('\n\nstopped')

        total_entropy, feature_entropies = get_entropies(dataset)

        # Step 3: Find the feature fk such that the difference between the
        #   total entropy and feature entropy for fk is minimum.
        entropy_difference = np.subtract(total_entropy, feature_entropies)
        print('\n entropy_difference: ', dataset)

        #       need feature index

        # Step 4: Exclude feature fk from the dataset and record it as the
        #   "least contributing" feature.
        # exclude[fk] = True
        # print(column name of fk)

        # Step 5: Repeat steps 2–4 until there is only one feature in F.
        # if (there is only one unexcluded feature in exclude):
        break

    # Step 6: Report the last remaining feature is the "most contributing" feature.
    # print(that last remaining fk)

    return None


def get_entropies(dataset):

    features = len(dataset[0])
    instances = len(dataset)

    sample_differences = [
    np.subtract(dataset[i], dataset[j])
    for i in range(instances-1)
    for j in range(i+1, instances)
    ]

    zip_ds = zip(*dataset)
    max_values = [max(r) for r in [list(d) for d in zip_ds]]
    min_values = [min(r) for r in [list(d) for d in zip_ds]]

    value_ranges = [
    np.subtract(max_values[k], min_values[k])
    for k in range(features)
    ]

    normalized = np.divide(sample_differences, value_ranges)

    # Calculate total entropy
    sample_distances = np.sqrt(np.sum(np.square(normalized)))
    average_sample_distance = np.average(sample_distances)
    alpha = np.divide(- np.log(0.5), average_sample_distance)

    similarities = np.exp(np.multiply(-alpha, sample_distances))
    similarities = [i for i in similarities if i not in [1.0]]
    dissimilarities = np.subtract(1.0, similarities)

    pairwise_entropies = 
    np.add(
    np.multiply(similarities, np.log10(similarities)), 
    np.multiply(dissimilarities, np.log10(dissimilarities))
    )

    total_entropy = - np.sum(pairwise_entropies)

    # Calculate feature entropies
    x = np.absoulte(normalized)

    return total_entropy, feature_entropies


if __name__ == '__main__':

    print('\nCheck unaccelerated Feature Ranking on console...\n')

    datasets_list = discover_datasets()
    for ds in datasets_list:
        print(ds['short_name'], '  ', end='')

    ds_name = input('\n\nChose a dataset: ').lower()
    ds_info = next((d for d in datasets_list if d['short_name'] == ds_name), None)

    if ds_info is not None:
        ranking_protocol(ds_info)
