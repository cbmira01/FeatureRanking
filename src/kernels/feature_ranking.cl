
//
// OpenCL kernels to solve entropic measure feature ranking
//

// ---------------------------------------------------------------------

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

// ---------------------------------------------------------------------

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

// ---------------------------------------------------------------------

__kernel void normalized_differences(
    __global float *sample_differences_g, 
    __global float *value_ranges_g,
    const int num_cols,
    const int num_rows, 
    __global float *normalized_differences_g)
{ 
    int k = get_global_id(0); // range over columns
    int row, addr;

    for (row = 0; row < num_rows; row++) {
        addr = row * num_cols + k;
        normalized_differences_g[addr] = 
            sample_differences_g[addr] / value_ranges_g[k];
    }
}

// ---------------------------------------------------------------------

__kernel void sample_distances(
    __global float *normalized_differences_g, 
    const int num_cols,
    __global float *sample_distances_g) 
{ 
    int row = get_global_id(0); // range over rows
    float sum_squares = 0.0f;

    for (int col = 0; col < num_cols; col++) {
        sum_squares = sum_squares + pown(normalized_differences_g[row * num_cols + col], 2);
    }

    sample_distances_g[row] = sqrt(sum_squares);
}

// ---------------------------------------------------------------------


// Thanks to lecture notes "Introduction to OpenCL" by George Leaver, June 2012 
// http://wiki.rac.manchester.ac.uk/community/OpenCL?action=AttachFile&do=get&target=IntrotoOpenCL.pdf

__kernel void sum_array( 
    __global const float *input_g, // assuming len(input_g) is a power of two
    const int num_rows, 
    __global float *partial_sums_g,
    __global float *result_g)
{ 
    __local float local_sums[128];

    int global_id = get_global_id(0);
    int local_id = get_local_id(0);
    int group_id = get_group_id(0);
    int group_size = get_local_size(0);

    local_sums[local_id] = input_g[global_id];

    for(int stride = group_size / 2; stride > 1; stride /= 2) { 
        barrier(CLK_GLOBAL_MEM_FENCE | CLK_LOCAL_MEM_FENCE);

        if(local_id < stride)
            local_sums[local_id] += local_sums[local_id + stride];
    } 

    if(local_id == 0) {
        partial_sums_g[group_id] = local_sums[0];
    }

    // Reduce the partial sums
    float sum;

    if(local_id == 0) {
        sum = partial_sums_g[0];
        for(int i = 1; i <  get_num_groups(0); i++)
            sum += partial_sums_g[i];

        result_g[0] = sum; 
        result_g[1] = (float)get_global_size(0);
        result_g[2] = (float)get_local_size(0);
        result_g[3] = (float)get_num_groups(0);
    }
}

// ---------------------------------------------------------------------

__kernel void pairwise_entropies(
    __global float *sample_distances_g, 
    
    // alpha is a scaling factor to expand very small average sample distances
    const float alpha, 

    const int num_rows,
    __global float *similarities_g,
    __global float *dissimilarities_g,
    __global float *pairwise_entropies_g)
{ 
    int gid = get_global_id(0);

    similarities_g[gid] = exp((-alpha * sample_distances_g[gid]));
    dissimilarities_g[gid] = 1.0f - similarities_g[gid];

    pairwise_entropies_g[gid] = 
        (similarities_g[gid] * log10(similarities_g[gid]))
        + (dissimilarities_g[gid] * log10(dissimilarities_g[gid]));
}

