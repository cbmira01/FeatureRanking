
//
// OpenCL kernels to solve entropic measure feature ranking
//

__kernel void sample_differences( 
   __global float *dataset_g, 
   const int features, 
   const int instances,
   __global float *result_g) 
{ 
    int k, row; 
    int i = get_global_id(0); # dataset row i
    int j = get_global_id(1); # dataset row j

    if (i < j) # ( (n^2 - n) / 2 ) row comparisons
    {
        for (k = 0; k < features; k++) {
            row = # some function of i,j, and instances, zero-based
            result_g[row*features + k] = 
                dataset_g[i*features + k] - dataset_g[j*features + k]; 
        }
    }
}

// result_g layout for sample_differences:
// idx = (2 * i * n - i ** 2 + 2 * j - 3 * i - 2) / 2

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
