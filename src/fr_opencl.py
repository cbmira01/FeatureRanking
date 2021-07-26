
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

    # Prepare the context, command queue and program for the current device
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

        remaining_entropy = get_entropy_opencl(remaining_dataset, context, program)

        # Step 2b: Find the entropies of each non-excluded feature.
        columns = np.array(dataset).transpose().tolist()
        feature_entropies = [] # for debugging
        entropy_differences = []

        for k in range(features):
            if exclude[k]:
                feature_entropies.append(None)
                entropy_differences.append(float('inf')) # force no test here
            else:
                fe = get_entropy_opencl([[c] for c in columns[k]], context, program)
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

    # ------------------------------------------------------------------

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

    # cl.enqueue_copy(queue, sample_differences_np, sample_differences_g)
    breakpoint()

    # ------------------------------------------------------------------

    # zip_ds = [list(d) for d in zip(*dataset)]
    # max_values = [max(r) for r in zip_ds]
    # min_values = [min(r) for r in zip_ds]
    # value_ranges = np.subtract(max_values, min_values)

    min_values_g = cl.Buffer(ctx, mf.READ_WRITE, np.empty([features]).astype(np.float32).nbytes)
    max_values_g = cl.Buffer(ctx, mf.READ_WRITE, np.empty([features]).astype(np.float32).nbytes)

    value_ranges_np = np.empty([features]).astype(np.float32)
    value_ranges_g = cl.Buffer(ctx, mf.READ_WRITE, value_ranges_np.nbytes)

    program.min_max_values(
        queue, (features,), None, 
        dataset_g, 
        np.int32(features),
        np.int32(instances), 
        min_values_g,
        max_values_g,
        value_ranges_g)

    # cl.enqueue_copy(queue, value_ranges_np, value_ranges_g)
    # breakpoint()

    # ------------------------------------------------------------------

    # normalized_differences = np.divide(sample_differences, value_ranges)

    num_rows, num_cols = np.shape(sample_differences_np)
    normalized_differences_np = np.empty([num_rows, num_cols]).astype(np.float32)
    normalized_differences_g = cl.Buffer(ctx, mf.READ_WRITE, normalized_differences_np.nbytes)

    program.normalized_differences(
        queue, (num_cols,), None, 
        sample_differences_g, 
        value_ranges_g,
        np.int32(num_cols),
        np.int32(num_rows), 
        normalized_differences_g)

    # cl.enqueue_copy(queue, normalized_differences_np, normalized_differences_g)
    # breakpoint()

    # ------------------------------------------------------------------

    # sample_distances = np.sqrt([np.sum(s) for s in np.square(normalized_differences)])
    # sample_distances = [sd for sd in sample_distances if sd != 0] # avoid zero distances

    num_rows, num_cols = np.shape(normalized_differences_np)
    sample_distances_np = np.empty([num_rows]).astype(np.float32)
    sample_distances_g = cl.Buffer(ctx, mf.READ_WRITE, sample_distances_np.nbytes)

    program.sample_distances(
        queue, (num_rows,), None, 
        normalized_differences_g, 
        np.int32(num_cols),
        sample_distances_g)

    cl.enqueue_copy(queue, sample_distances_np, sample_distances_g)

    # Filter out zero distances; OpenCL does not build variable-length arrays
    sample_distances_np = np.array([sd for sd in sample_distances_np if sd != 0])

    # ------------------------------------------------------------------

    # average_sample_distance = np.average(sample_distances)
    average_sample_distance = np.average(sample_distances_np)

    # bite_size = 128 # this should be derived from device properties
    # padded_distances_np = pad_for_sum(sample_distances_np, bite_size)
    # padded_distances_g = cl.Buffer(ctx, mf.READ_WRITE, padded_distances_np.nbytes)
    # num_rows = len(padded_distances_np)

    # partials_np = np.empty([num_rows//bite_size]).astype(np.float32)
    # partials_g = cl.Buffer(ctx, mf.READ_WRITE, partials_np.nbytes)

    # result_np = np.empty([4]).astype(np.float32)
    # result_g = cl.Buffer(ctx, mf.READ_WRITE, result_np.nbytes)

    # program.sum_array(queue, (num_rows,), None, padded_distances_g, np.int32(num_rows), partials_g, result_g)

    # cl.enqueue_copy(queue, result_np, result_g)
    # average_sample_distance = np.divide(result_np[0], len(sample_distances_np));

    # cl.enqueue_copy(queue, partials_np, partials_g)
    # print(result_np, 'avg = ', average_sample_distance)
    # breakpoint()

    # ------------------------------------------------------------------

    alpha = np.divide(- np.log(0.5), average_sample_distance)
    # breakpoint()

    # ------------------------------------------------------------------

    # similarities = np.exp(np.multiply(-alpha, sample_distances))
    # dissimilarities = np.subtract(1, similarities)

    # pairwise_entropies = np.add(
    # np.multiply(similarities, np.log10(similarities)),
    # np.multiply(dissimilarities, np.log10(dissimilarities))
    # )

    similarities_g = cl.Buffer(ctx, mf.READ_WRITE, np.empty(num_rows).astype(np.float32).nbytes)
    dissimilarities_g = cl.Buffer(ctx, mf.READ_WRITE, np.empty(num_rows).astype(np.float32).nbytes)

    pairwise_entropies_np = np.empty(num_rows).astype(np.float32)
    pairwise_entropies_g = cl.Buffer(ctx, mf.READ_WRITE, pairwise_entropies_np.nbytes)

    program.pairwise_entropies(
        queue, (num_rows,), None, 
        sample_distances_g, 
        np.float32(alpha),
        np.int32(num_rows),
        similarities_g,
        dissimilarities_g,
        pairwise_entropies_g)
    
    cl.enqueue_copy(queue, pairwise_entropies_np, pairwise_entropies_g)
    # breakpoint()

    # ------------------------------------------------------------------

    # entropy = - np.sum(pairwise_entropies)
    entropy = - np.sum(pairwise_entropies_np)

    return entropy


def pad_for_sum(arr, wgs):
    # This function is needed to facilitate efficient summing of arrays
    # wgs is work-group size, should be a power of two

    leftover = np.remainder(len(arr), wgs)
    zeros = np.zeros(wgs - leftover, dtype=arr.dtype)
    arr = np.concatenate([arr, zeros])
    return arr


if __name__ == '__main__':

    print('\nCheck OpenCL Feature Ranking at console...\n')

    datasets_list = discover_datasets()
    for ds in datasets_list:
        print(ds['short_name'], '  ', end='')

    ds_name = input('\n\nChose a dataset: ').lower()
    ds_info = next((d for d in datasets_list if d['short_name'] == ds_name), None)

    if ds_info is not None:
        opencl_device_driver(ds_info)
