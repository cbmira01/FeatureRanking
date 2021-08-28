
# 
# This script knows how to find OpenCL devices, compile CL programs, 
#   and build OpenCL execution contexts.

import pyopencl as cl

devtype_readable = { 
    "1": "DEFAULT",
    "2": "CPU",
    "4": "GPU",
    "8": "ACCELERATOR",
    "16": "CUSTOM",
    }

def discover_devices():

    devices = []
    opencl_device_available = False

    for platform in cl.get_platforms():
        for device in platform.get_devices(cl.device_type.ALL):
            opencl_device_available = True
            devices.append(device)

    return opencl_device_available, devices

if __name__ == '__main__':

    available, devices = discover_devices()

    print('\nOpenCL devices available:')
    for device in devices:
        print('    ', device)

    print('\n')
    print('OpenCL device available? ', 'Yes' if bool(available) else 'No')
