
#
# This is the unaccelerated Feature Ranking implementation
#

import numpy as np
import sys
import time

def get_entropy(dataset):

    start_time = time.perf_counter()

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

    stop_time = time.perf_counter()

    return stop_time - start_time, entropy


if __name__ == '__main__':

    print('\n\nRun the main program via: python feature_ranking\n')

