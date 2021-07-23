
//
// OpenCL kernels to solve entropic measure feature ranking
//

__kernel void sample_differences( 
   __global float *dataset_g, 
   const int features, 
   const int instances,
   __global float *sample_differences_g) 
{ 
    int k, new_row; 
    int i = get_global_id(0); // dataset row i
    int j = get_global_id(1); // dataset row j

    // ((instances^2 - instances) / 2) new rows will result here
    if (i < j) 
    {
        for (k = 0; k < features; k++) {
            // Thanks to https://math.stackexchange.com/a/646125 for new row address scheme
            new_row = (2 * i * instances - i * i + 2 * j - 3 * i - 2) / 2;
            sample_differences_g[new_row * features + k] = 
                dataset_g[i * features + k] - dataset_g[j * features + k]; 
        }
    }
}

__kernel void min_max_values(
    __global float *dataset_g, 
    const int features, 
    const int instances,
    __global float *min_values_g,
    __global float *max_values_g,
    __global float *value_ranges_g) 
{
    int row;
    float cur_val;
    int k = get_global_id(0); // range over features

    min_values_g[k] = dataset_g[k];
    max_values_g[k] = dataset_g[k];

    for (row = 1; row < instances; row++) {

        cur_val = dataset_g[row * features + k];

        if (cur_val < min_values_g[k])
            min_values_g[k] = cur_val;

        if (cur_val > max_values_g[k])
            max_values_g[k] = cur_val;
    }

    mem_fence(CLK_GLOBAL_MEM_FENCE); // finish prior calculations

    value_ranges_g[k] = max_values_g[k] - min_values_g[k];
}

// __kernel void value_ranges(arguments) { }

// __kernel void normalized_differences(arguments) { }

// __kernel void sample_distances(arguments) { }

// __kernel void average_sample_distance(arguments) { }

// __kernel void similarities(arguments) { }

// __kernel void dissimilarities(arguments) { }

// __kernel void pairwise_entropies(arguments) { }

// __kernel void entropy(arguments) { }

// __kernel void name(arguments) { }
