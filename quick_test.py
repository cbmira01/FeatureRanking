
# A quick test of the PyOpenCL installation:
#   - dump information on available platforms and devices
#   - do a very small workload test on each device

import pyopencl as cl
import numpy as np

# Identify available OpenCL platforms and devices
platforms = cl.get_platforms()
print('\n')
print('OpenCL platform and device information...')
print('\n')
for platform in platforms:
    print('Platform name: ', platform.name.lstrip())
    
    devices = platform.get_devices(cl.device_type.ALL)
    for device in devices:
        print('\n    ', 'Device name: ', device.name.lstrip(), ' ', device.vendor.lstrip())    
        print('    ', 'Version:', device.version)
        print('    ', 'Available? ', bool(device.available))
        print('    ', 'Processor type: ', cl.device_type.to_string(device.type))
        print('    ', 'Local memory: ', device.local_mem_size)
        print('    ', 'Global memory: ', device.global_mem_size)
        print('    ', 'Work group size: ', device.max_work_group_size)
        print('    ', 'Compute units: ', device.max_compute_units)


# Run small workloads on each device
# platforms = cl.get_platforms()
# for platform in platforms:  
    # devices = platform.get_devices(cl.device_type.ALL)
    # for device in devices:


first_argument_np = np.random.rand(5).astype(np.float32)
second_argument_np = np.random.rand(5).astype(np.float32)

context = cl.create_some_context(interactive=True)
command_queue = cl.CommandQueue(context)
memory_flags = cl.mem_flags

first_argument_g = cl.Buffer(
    context, 
    memory_flags.READ_ONLY | memory_flags.COPY_HOST_PTR, 
    hostbuf=first_argument_np)
    
second_argument_g = cl.Buffer(
    context, 
    memory_flags.READ_ONLY | memory_flags.COPY_HOST_PTR, 
    hostbuf=second_argument_np)

with open('./kernels/small_multiply.cl', 'r') as kernel_file:
    kernel_source = kernel_file.read()
program = cl.Program(context, kernel_source).build()

result_g = cl.Buffer(
    context, 
    memory_flags.WRITE_ONLY, 
    first_argument_np.nbytes)

program.add(
    command_queue, 
    first_argument_np.shape, 
    None, 
    first_argument_g, 
    second_argument_g, 
    result_g)

result_np = np.empty_like(first_argument_np)
cl.enqueue_copy(command_queue, result_np, result_g)

print('\n')
print(' ', first_argument_np)
print('+', second_argument_np)
print('=', result_np)
