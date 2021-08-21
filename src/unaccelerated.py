
#
# This is the unaccelerated Feature Ranking implementation
#

import numpy as np
import sys
from prepare_data import *
import time

def ranking_protocol(dataset_info):

    # The ranking protocol will rank dataset features from the "least important"
    #   to the "most important", in the sense that low-ranking features
    #   contribute the least "surprisal" to the remaining dataset to which they
    #   being compared. In each round, the protocol will identify the least
    #   contributing feature, then drop it from consideration in following
    #   rounds.

    dataset = get_clean_data(dataset_info, dump=False)
    label_names = get_label_names(dataset_info)
    print('\n')
    print('Trial on unaccelerated CPU')
    print('Dataset: ', dataset_info['long_name'])
    if (False): # configuration
        print('Label names: ', label_names)

    ranking_start = time.perf_counter()

    # Step 1: Start with an initial full set of features (no exclusions).
    instances = len(dataset)
    features = len(dataset[0])
    exclude = [False for k in range(features)]
    counter = 1

    while True:
        # Step 2a: Find the total entropy of the remaing dataset.
        remaining_dataset = []

        for row in dataset:
            remaining_dataset.append([row[k] for k in range(features) if not exclude[k]])

        remaining_entropy = get_entropy(remaining_dataset)

        # Step 2b: Find the entropies of each non-excluded feature.
        columns = np.array(dataset).transpose().tolist()
        feature_entropies = [] # for debugging
        entropy_differences = []

        for k in range(features):
            if exclude[k]:
                feature_entropies.append(None)
                entropy_differences.append(float('inf')) # force no test here
            else:
                fe = get_entropy([[c] for c in columns[k]])
                feature_entropies.append(fe)
                ed = np.absolute(np.subtract(remaining_entropy, fe))
                entropy_differences.append(ed)

        # Step 3: Find the feature fk such that the difference between the
        #   total entropy and feature entropy for fk is minimum.
        drop_index = entropy_differences.index(min(entropy_differences))

        # Step 4: Exclude feature fk from the dataset and report it as the
        #   "least contributing" feature.
        exclude[drop_index] = True

        print('   Round', counter, ', dropped', label_names[drop_index], end='')
        print(', remaining entropy', remaining_entropy)
        if (False): # configuration
            print('    Entropy differences: ', entropy_differences)
        sys.stdout.flush() 

        # Step 5: Repeat steps 2–4 until no features remain.
        counter = counter + 1
        if exclude.count(False) == 0:
            break

    ranking_stop = time.perf_counter()
    print(f"Ranking completed in {ranking_stop - ranking_start:0.2f} seconds")

    return None


def get_entropy(dataset):

    features = len(dataset[0])
    instances = len(dataset)

    sample_differences = [
    np.subtract(dataset[i], dataset[j])
    for i in range(instances-1)
    for j in range(i+1, instances)
    ]

    zip_ds = [list(d) for d in zip(*dataset)]
    max_values = [max(r) for r in zip_ds]
    min_values = [min(r) for r in zip_ds]
    value_ranges = np.subtract(max_values, min_values)

    normalized_differences = np.divide(sample_differences, value_ranges)

    # Calculate total entropy
    sample_distances = np.sqrt([np.sum(s) for s in np.square(normalized_differences)])
    sample_distances = [sd for sd in sample_distances if sd != 0] # avoid zero distances

    average_sample_distance = np.average(sample_distances)
    alpha = np.divide(- np.log(0.5), average_sample_distance)

    similarities = np.exp(np.multiply(-alpha, sample_distances))
    dissimilarities = np.subtract(1, similarities)

    pairwise_entropies = np.add(
    np.multiply(similarities, np.log10(similarities)),
    np.multiply(dissimilarities, np.log10(dissimilarities))
    )

    entropy = - np.sum(pairwise_entropies)

    return entropy


if __name__ == '__main__':

    print('\nCheck unaccelerated Feature Ranking on console...\n')

    datasets_list = discover_datasets()
    for ds in datasets_list:
        print(ds['short_name'], '  ', end='')

    ds_name = input('\n\nChose a dataset: ').lower()
    ds_info = next((d for d in datasets_list if d['short_name'] == ds_name), None)

    if ds_info is not None:
        ranking_protocol(ds_info)
