
#
# This is the host program for the OpenCL implementation of Feature Ranking
#

import pyopencl as cl
import numpy as np
import sys
from prep_data import *

def opencl_device_driver(dataset_info):

    for platform in cl.get_platforms():
        for device in platform.get_devices(cl.device_type.ALL):
            print([device], '\n')
            ranking_protocol(dataset_info, device)

    return None


def ranking_protocol(dataset_info, device):

    # Prepare the context, command queue and program  for the current device
    with open('./kernels/feature_ranking.cl', 'r') as f:
        kernel_source = f.read()

    context = cl.Context([device])

    try: 
        program = cl.Program(context, kernel_source).build()
    except:
        print('\n\n      There was an error while building the kernel...')
        e = sys.exc_info()
        print('\nError type: ', e[0])
        print('\nError value: \n', e[1])
        # print('\nError traceback: ', e[2])
        sys.exit()

    dataset1 = [
    [3, 2, 1],
    [2, 4, 3],
    [5, 3, 9]
    ]

    dataset2 = [
    [0.34818205,0.0054406016,0.17633587,0.010881203,2.5290077],
    [0.9478498,0.8079211,0.9687416,1.6158422,4.9062247],
    [0.2887636,0.450703,0.29179972,0.901406,2.875399],
    [0.62086165,0.59616053,0.09807767,1.1923211,2.294233],
    [0.017327862,0.823534,0.6032455,1.647068,3.8097365],
    [0.06374773,0.86418086,0.9055053,1.7283617,4.716516],
    [0.33667052,0.23504795,0.6865279,0.4700959,4.0595837],
    [0.82834285,0.35440725,0.123982616,0.7088145,2.3719478],
    [0.92590517,0.41533554,0.62911564,0.8306711,3.887347],
    [0.5316418,0.52066636,0.3490727,1.0413327,3.047218]
    ]

    label_names1 = [
        "F1",
        "F2",
        "F3",
    ]

    label_names2 = [
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "C6",
        "C7",
        "C8"
    ]

    print(label_names1)
    # print(*dataset1,sep='\n')
    print('\n')
    print(label_names2)
    # print(*dataset2,sep='\n')

    # ------------------------------------

    dataset = dataset2
    label_names = label_names2

    # for now, call entropy calculation here
    get_entropy_opencl(dataset, context, program)

    sys.exit()
    # ------------------------------------

    print('\n')
    print('Dataset: ', dataset_info['long_name'])
    print('Label names: ', label_names)
    print('OpenCL device:', device)

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

        print('\nRound', counter, ', dropped', label_names[drop_index])
        print('    Remaining entropy:   ', remaining_entropy)
        print('    Entropy differences: ', entropy_differences)
        sys.stdout.flush() 

        # Step 5: Repeat steps 2–4 until no features remain.
        counter = counter + 1
        if exclude.count(False) == 0:
            break

    return None


def get_entropy_opencl(dataset, context, program):

    # OpenCL execution context and compiled program on hand
    mem_flags = cl.mem_flags
    command_queue = cl.CommandQueue(context)

    # Marshal Python-hosted data into the device global data area

    # Designate a portion of the global data to hold result of computation

    # Call the kernel on global arguments

    # Marshal computation results into a Python-hosted array

    # ------------------------------------------------------------------

    # features = len(dataset[0])
    # instances = len(dataset)

    # sample_differences = [
    # np.subtract(dataset[i], dataset[j])
    # for i in range(instances-1)
    # for j in range(i+1, instances)
    # ]

    # zip_ds = [list(d) for d in zip(*dataset)]
    # max_values = [max(r) for r in zip_ds]
    # min_values = [min(r) for r in zip_ds]
    # value_ranges = np.subtract(max_values, min_values)

    # normalized_differences = np.divide(sample_differences, value_ranges)

    # Calculate total entropy
    # sample_distances = np.sqrt([np.sum(s) for s in np.square(normalized_differences)])
    # sample_distances = [sd for sd in sample_distances if sd != 0] # avoid zero distances

    # average_sample_distance = np.average(sample_distances)
    # alpha = np.divide(- np.log(0.5), average_sample_distance)

    # similarities = np.exp(np.multiply(-alpha, sample_distances))
    # dissimilarities = np.subtract(1, similarities)

    # pairwise_entropies = np.add(
    # np.multiply(similarities, np.log10(similarities)),
    # np.multiply(dissimilarities, np.log10(dissimilarities))
    # )

    # entropy = - np.sum(pairwise_entropies)

    return None


if __name__ == '__main__':

    print('\nCheck OpenCL Feature Ranking at console...\n')

    datasets_list = discover_datasets()
    for ds in datasets_list:
        print(ds['short_name'], '  ', end='')

    ds_name = input('\n\nChose a dataset: ').lower()
    ds_info = next((d for d in datasets_list if d['short_name'] == ds_name), None)

    if ds_info is not None:
        opencl_device_driver(ds_info)
