
# A quick test of the PyOpenCL installation:
#   - dump information on available platforms and devices
#   - do a very small workload test on each device

import pyopencl as cl
import numpy as np

print('\n')
print('OpenCL platforms and devices discovered on this workstation...\n')

for platform in cl.get_platforms():
    print('Platform name: ', platform.name.lstrip())
    
    for device in platform.get_devices(cl.device_type.ALL):
        print('    ', 'Device name: ', device.name.lstrip())
        print('    ', 'Vendor: ', device.vendor.lstrip())    
        print('    ', 'Version:', device.version)
        print('    ', 'Available? ', bool(device.available))
        print('    ', 'Processor type: ', cl.device_type.to_string(device.type))
        print('    ', 'Local memory: ', device.local_mem_size)
        print('    ', 'Global memory: ', device.global_mem_size)
        print('    ', 'Work group size: ', device.max_work_group_size)
        print('    ', 'Compute units: ', device.max_compute_units)
        print('\n')

print('Running small workloads on each device...\n')

# Fetch the OpenCL source code to run for this exercise
with open('./kernels/quick_test.cl', 'r') as f:
    kernel_source = f.read()

for platform in cl.get_platforms():
    for device in platform.get_devices(cl.device_type.ALL):
        print([device], '\n')

        # Prepare Python-hosted data
        first_argument_np = np.random.rand(5).astype(np.float32)
        second_argument_np = np.random.rand(5).astype(np.float32)
        print(' ', first_argument_np)
        print('+', second_argument_np)

        # Prepare the context and command queue for the current device
        context = cl.Context([device])
        command_queue = cl.CommandQueue(context)
        memory_flags = cl.mem_flags

        # Compile the OpenCL program into an executable kernel
        program = cl.Program(context, kernel_source).build()

        # Marshal Python-hosted data into the device global data areas
        first_argument_g = cl.Buffer(
            context, 
            memory_flags.READ_ONLY | memory_flags.COPY_HOST_PTR, 
            hostbuf=first_argument_np)
        second_argument_g = cl.Buffer(
            context, 
            memory_flags.READ_ONLY | memory_flags.COPY_HOST_PTR, 
            hostbuf=second_argument_np)

        # Designate a portion of the global data area to hold the result of computation
        result_g = cl.Buffer(context, memory_flags.WRITE_ONLY, first_argument_np.nbytes)

        # Call the kernel method on global arguments
        program.add(
            command_queue, 
            first_argument_np.shape, 
            None, 
            first_argument_g, 
            second_argument_g, 
            result_g)

        # Marshal computation results back into Python-hosted area
        result_np = np.empty_like(first_argument_np)
        cl.enqueue_copy(command_queue, result_np, result_g)

        # Dump the results
        print('=', result_np)
        print('\n')