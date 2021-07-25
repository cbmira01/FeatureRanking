
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

__kernel void sum_distances(  
    __global float *distances_g,
    const int num_rows, 
    __global float *sums_g)
{
    __local float local_workspace[128];

    int global_id = get_global_id(0);
    int local_id = get_local_id(0);
    int group_id = get_group_id(0);
    int local_size = get_local_size(0); 

    int i;
    float sum;

    local_workspace[local_id] = distances_g[global_id];

    barrier(CLK_LOCAL_MEM_FENCE);

    if(local_id == 0) {
        sum = distances_g[0];

        for(i = 1; i < local_size; i++) {
            sum = sum + local_workspace[i];
        }

        sums_g[group_id] = sum; 
    }
} 

// ---------------------------------------------------------------------

// __kernel void similarities(arguments) { }

// ---------------------------------------------------------------------

// __kernel void pairwise_entropies(arguments) { }

// ---------------------------------------------------------------------

// __kernel void entropy(arguments) { }

