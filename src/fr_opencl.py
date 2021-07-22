
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
            print(device, '\n')
            ranking_protocol(dataset_info, device)

    return None


def ranking_protocol(dataset_info, device):

    # Prepare the context, command queue and program  for the current device
    context = cl.Context([device])

    try: 
        with open('./kernels/feature_ranking.cl', 'r') as f:
            kernel_source = f.read()

        program = cl.Program(context, kernel_source).build()
    except:
        print('\n\n      There was an error while building the kernel...')
        e = sys.exc_info()
        print('\nError type: ', e[0])
        print('\nError value: \n', e[1]) # contents of .get_build_info LOG
        # print('\nError traceback: ', e[2])
        sys.exit()

    dataset = get_clean_data(dataset_info, dump=False)
    label_names = get_label_names(dataset_info)

    print('\n')
    print('Trial on OpenCL device: ', device)
    print('Dataset: ', dataset_info['long_name'])
    print('Label names: ', label_names)

    # for now, call entropy calculation here
    get_entropy_opencl(dataset, context, program)
    sys.exit()

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


def get_entropy_opencl(dataset, ctx, program):

    # OpenCL execution context and compiled program on hand
    mf = cl.mem_flags
    queue = cl.CommandQueue(ctx)

    features = len(dataset[0])
    instances = len(dataset)

    # Sample Differences

    # sample_differences = [
    # np.subtract(dataset[i], dataset[j])
    # for i in range(instances-1)
    # for j in range(i+1, instances)
    # ]

    dataset_np = np.array(dataset).astype(np.float32)
    dataset_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=dataset_np)

    sample_differences_np = np.empty([(instances ** 2 - instances) // 2, features]).astype(np.float32)
    sample_differences_g = cl.Buffer(ctx, mf.WRITE_ONLY, sample_differences_np.nbytes)

    program.sample_differences(
        queue, (instances, instances), None, 
        dataset_g, np.int32(features), np.int32(instances), 
        sample_differences_g)

    cl.enqueue_copy(queue, sample_differences_np, sample_differences_g)
    breakpoint()
    # ------------------------------------------------------------------


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
