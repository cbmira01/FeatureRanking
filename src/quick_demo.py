
#
# A quick demonstration of the PyOpenCL installation:
#   - dump information on available platforms and devices
#   - do a very small workload test on each device
#
# This program was built using examples from:
#   - "Hands On OpenCL" (http://handsonopencl.github.io/)
#   - Code examples from the PyOpenCL project (https://github.com/inducer/pyopencl)
#   - pyopencl-in-action (https://github.com/oysstu/pyopencl-in-action)
#

import sys
import pyopencl as cl
import numpy as np
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

devtype_readable = { 
    "1": "DEFAULT",
    "2": "CPU",
    "4": "GPU",
    "8": "ACCELERATOR",
    "16": "CUSTOM",
    }

print('\n')
print('OpenCL platforms and devices discovered on this workstation...\n')

device_available = False

for platform in cl.get_platforms():

    print('Platform name: ', platform.name.lstrip())

    for device in platform.get_devices(cl.device_type.ALL):
        device_available = True

        print('    Device name: ', device.name.lstrip())
        print('        Vendor: ', device.vendor.lstrip())
        print('        Version:', device.version)
        print('        Device available? ', 'Yes' if bool(device.available) else 'No')
        print('        Compiler available? ', 'Yes' if bool(device.compiler_available) else 'No')
        print('        Processor type: ', devtype_readable.get(str(device.type), "Unknown..."))
        print('        Compute units: ', device.max_compute_units)
        print('        Global memory: ', format(device.global_mem_size, '>1,d'), 'bytes')
        print('        Local memory: ', format(device.local_mem_size, '>1,d'), 'bytes')
        print('        Max work group size: ', device.max_work_group_size, 'work items')
        print('        Max work item dimensions: ', device.max_work_item_dimensions)
        print('        Max work item sizes: ', device.max_work_item_sizes)

if device_available == False:
    print('No OpenCL devices were discovered on this workstation')
    sys.exit()


# Prepare Python-hosted arrays
array_size = 1_000_000
first_argument_np = np.random.rand(array_size).astype(np.float32)
second_argument_np = np.random.rand(array_size).astype(np.float32)
result_np = np.empty(array_size).astype(np.float32)

print(f'\nRunning a small workload on each device: ', format(array_size, '>1,d'), 'multiplications \n')

# Fetch the OpenCL source code to run for this exercise
with open('./kernels/quick_test.cl', 'r') as f:
    kernel_source = f.read()

for platform in cl.get_platforms():
    for device in platform.get_devices(cl.device_type.ALL):
        print(device)
        print('    ', first_argument_np)
        print('   *', second_argument_np)

        # Prepare the context and command queue for the current device
        context = cl.Context([device])
        command_queue = cl.CommandQueue(context)
        memory_flags = cl.mem_flags

        # Compile the OpenCL program
        program = cl.Program(context, kernel_source).build()

        # Marshal Python-hosted data into the device global data area
        first_argument_g = cl.Buffer(
            context,
            memory_flags.READ_ONLY | memory_flags.COPY_HOST_PTR,
            hostbuf=first_argument_np)
        second_argument_g = cl.Buffer(
            context,
            memory_flags.READ_ONLY | memory_flags.COPY_HOST_PTR,
            hostbuf=second_argument_np)

        # Designate a portion of the global data area
        #   to hold the result of computation
        result_g = cl.Buffer(
            context,
            memory_flags.WRITE_ONLY,
            first_argument_np.nbytes)

        # Call the kernel on global arguments
        program.add(
            command_queue,
            first_argument_np.shape,
            None,
            first_argument_g,
            second_argument_g,
            result_g)

        # Marshal computation results into a Python-hosted array
        cl.enqueue_copy(command_queue, result_np, result_g)

        # Dump the results
        print('   =', result_np)
        print('\n')
