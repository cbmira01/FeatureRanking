
#
# A quick test of the PyOpenCL installation:
#   - dump information on available platforms and devices
#   - do a very small workload test on each device
#
# This program was built using examples from:
#   - "Hands On OpenCL" (http://handsonopencl.github.io/)
#   - Code examples from the PyOpenCL project (https://github.com/inducer/pyopencl)
#   - pyopencl-in-action (https://github.com/oysstu/pyopencl-in-action)
#

import pyopencl as cl
import numpy as np

devtype_readable = { 
    "1": "DEFAULT",
    "2": "CPU",
    "4": "GPU",
    "8": "ACCELERATOR",
    "16": "CUSTOM",
    }

print('\n')
print('OpenCL platforms and devices discovered on this workstation...\n')

for platform in cl.get_platforms():
    print('Platform name: ', platform.name.lstrip())

    for device in platform.get_devices(cl.device_type.ALL):
        print('    ', 'Device name: ', device.name.lstrip())
        print('    ', 'Vendor: ', device.vendor.lstrip())
        print('    ', 'Version:', device.version)
        print('    ', 'Available? ', bool(device.available))
        print('    ', 'Processor type: ', 
            devtype_readable.get(str(device.type), "Unknown..."))
        print('    ', 'Local memory: ', device.local_mem_size)
        print('    ', 'Global memory: ', device.global_mem_size)
        print('    ', 'Work group size: ', device.max_work_group_size)
        print('    ', 'Compute units: ', device.max_compute_units)
        print('\n')

print('Running a small workload on each device...\n')

# Fetch the OpenCL source code to run for this exercise
with open('./kernels/quick_test.cl', 'r') as f:
    kernel_source = f.read()

for platform in cl.get_platforms():
    for device in platform.get_devices(cl.device_type.ALL):
        print([device], '\n')

        # Prepare Python-hosted arrays
        array_size = 5
        first_argument_np = np.random.rand(array_size).astype(np.float32)
        second_argument_np = np.random.rand(array_size).astype(np.float32)
        result_np = np.empty(array_size).astype(np.float32)

        print('    ', first_argument_np)
        print('   +', second_argument_np)

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
