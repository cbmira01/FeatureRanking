
#
# This is the host program for the OpenCL implementation of Feature Ranking
#

import pyopencl as cl
import numpy as np
import sys


def get_entropy(dataset, ctx, program):

    # OpenCL execution context and compiled program on hand
    mf = cl.mem_flags
    queue = cl.CommandQueue(ctx)

    features = len(dataset[0])
    instances = len(dataset)

    dataset_np = np.array(dataset).astype(np.float32)
    dataset_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=dataset_np)

    sample_differences_np = np.empty([(instances ** 2 - instances) // 2, features]).astype(np.float32)
    sample_differences_g = cl.Buffer(ctx, mf.WRITE_ONLY, sample_differences_np.nbytes)

    program.sample_differences(
        queue, (instances, instances), None, 
        dataset_g, np.int32(features), np.int32(instances), 
        sample_differences_g)

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
    nonzero_sample_distances_np = np.array([sd for sd in sample_distances_np if sd != 0])

    # Figure out how to do this reduction on the OpenCL device
    average_sample_distance = np.average(sample_distances_np)
    alpha = np.divide(- np.log(0.5), average_sample_distance)

    num_rows = len(nonzero_sample_distances_np)
    nonzero_sample_distances_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=nonzero_sample_distances_np)

    similarities_g = cl.Buffer(ctx, mf.READ_WRITE, np.empty(num_rows).astype(np.float32).nbytes)
    dissimilarities_g = cl.Buffer(ctx, mf.READ_WRITE, np.empty(num_rows).astype(np.float32).nbytes)

    pairwise_entropies_np = np.empty(num_rows).astype(np.float32)
    pairwise_entropies_g = cl.Buffer(ctx, mf.READ_WRITE, pairwise_entropies_np.nbytes)

    program.pairwise_entropies(
        queue, (num_rows,), None, 
        nonzero_sample_distances_g, 
        np.float32(alpha),
        np.int32(num_rows),
        similarities_g,
        dissimilarities_g,
        pairwise_entropies_g)
    
    cl.enqueue_copy(queue, pairwise_entropies_np, pairwise_entropies_g)

    # Figure out how to do this reduction on the OpenCL device
    entropy = - np.sum(pairwise_entropies_np)

    return entropy


def pad_for_sum(array_to_pad, work_group_size):
    # This function is needed to facilitate efficient summing of arrays in OpenCL
    #     work_group_size should be a power of two

    leftover = np.remainder(len(array_to_pad), work_group_size)
    zeros = np.zeros(work_group_size - leftover, dtype=array_to_pad.dtype)
    return np.concatenate([array_to_pad, zeros])
