
//
// OpenCL kernels to solve entropic measure feature ranking
//

__kernel void sample_differences(
    __global float *dataset_g, 
    int rows_g,
    int columns_g,
    __global float *result_g) 
{
    int i, j, r;
    int gid = get_global_id(0);
    
    r = 0;
    for (i = 0; i < rows_g - 1; ++i)
        for (j = i + 1; i < rows_g; ++j)
            result_g[r * rows_g + gid] = 
                dataset_g[i * rows_g + gid] - dataset_g[j * rows_g + gid];
            r = r + i * rows_g + columns_g;
}

// __kernel void min_max_values(arguments) { }

// __kernel void value_ranges(arguments) { }

// __kernel void normalized_differences(arguments) { }

// __kernel void sample_distances(arguments) { }

// __kernel void average_sample_distance(arguments) { }

// __kernel void similarities(arguments) { }

// __kernel void dissimilarities(arguments) { }

// __kernel void pairwise_entropies(arguments) { }

// __kernel void entropy(arguments) { }

// __kernel void name(arguments) { }
