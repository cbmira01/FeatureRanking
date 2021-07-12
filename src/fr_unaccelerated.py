
#
# This is the unaccelerated Feature Ranking implementation
#

import numpy as np
import sys
from prep_data import *


def ranking_protocol(dataset_info):

    # The ranking protocol will rank dataset features from the "least important"
    #   to the "most important", in the sense that low-ranking features 
    #   contribute the least "surprisal" to the remaining dataset to which they 
    #   being compared. In each round, the protocol will identify the least
    #   contributing feature, then drop it from consideration in following
    #   rounds.
    
    dataset = get_clean_data(dataset_info, dump=False)

    # Step 1: Start with an initial full set of features (no exclusions).
    instances = len(dataset)
    features = len(dataset[0])
    exclude = [False for k in range(features)]
    exclude = [False, True, False]

    while True:
        # Step 2: Find the total entropy of the remaing dataset, and the
        #   feature entropies of each non-excluded feature.                
        
        remaining_dataset = []
        for row in dataset:
            remaining_dataset.append([row[k] for k in range(features) if not exclude[k]])
            
        total_entropy = get_entropy(remaining_dataset)
        
        feature_entropies = []
        columns = np.array(dataset).transpose().tolist()
        
        breakpoint()
        
        for k in range(features):
            if exclude[k]:
                feature_entropies.append(None)
            else:
                feature_entropies.append(get_entropy([[c] for c in columns[k]]))

        # Step 3: Find the feature fk such that the difference between the
        #   total entropy and feature entropy for fk is minimum.
        
        entropy_differences = np.absolute(np.subtract(total_entropy, feature_entropies)).tolist()
        drop_index = entropy_differences.index(min(entropy_differences))

        # Step 4: Exclude feature fk from the dataset and record it as the
        #   "least contributing" feature.
        # exclude[fk] = True
        # print(column name of fk)

        breakpoint()

        # Step 5: Repeat steps 2–4 until there is only one feature in F.
        if exclude.count(False) == 1:
            break

    # Step 6: Report the last remaining feature is the "most contributing" feature.
    # print(that last remaining fk)

    return None


def get_entropy(dataset):

    features = len(dataset[0])
    instances = len(dataset)

    sample_differences = [
    np.subtract(dataset[i], dataset[j])
    for i in range(instances-1)
    for j in range(i+1, instances)
    ]

    max_values = [max(r) for r in [list(d) for d in zip(*dataset)]]
    min_values = [min(r) for r in [list(d) for d in zip(*dataset)]]

    value_ranges = [
    np.subtract(max_values[k], min_values[k])
    for k in range(features)
    ]

    normalized = np.divide(sample_differences, value_ranges)

    # Calculate total entropy
    sample_distances = np.sqrt([np.sum(s) for s in np.square(normalized)])
    average_sample_distance = np.average(sample_distances)
    alpha = np.divide(- np.log(0.5), average_sample_distance)

    similarities = np.exp(np.multiply(-alpha, sample_distances))
    similarities = [s for s in similarities if s not in [1.0]]
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
