
# A quick test of the PyOpenCL installation:
#   - dump information on available platforms and devices
#   - do a very small workload test on each device

import pyopencl as cl

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
