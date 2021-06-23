
// OpenCL platfor quick test kernel
//   Perform an elementwise add on two small arrays

__kernel void add(
    __global const float *first_argument_g, 
    __global const float *second_argument_g, 
    __global float *result_g)
{
  int gid = get_global_id(0);
  result_g[gid] = first_argument_g[gid] + second_argument_g[gid];
}
