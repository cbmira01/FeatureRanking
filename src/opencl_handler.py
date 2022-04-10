
# 
# This script knows how to find OpenCL devices, compile CL programs, 
#   and build OpenCL execution contexts.

import pyopencl as cl
import sys

devtype_readable = { 
    "1": "DEFAULT",
    "2": "CPU",
    "4": "GPU",
    "8": "ACCELERATOR",
    "16": "CUSTOM",
    }

def discover_devices():

    devices = []

    for platform in cl.get_platforms():
        for device in platform.get_devices(cl.device_type.ALL):
            if device.available:
                devices.append(device)

    return devices


def get_context(device):
    return cl.Context([device])


def build_opencl_program(context):

    try: 
        with open('./kernels/feature_ranking.cl', 'r') as f:
            kernel_source = f.read()
        program = cl.Program(context, kernel_source).build()
    except:
        print('\n\n      There was an error while building the OpenCL program...')
        e = sys.exc_info()
        print('\nError type: ', e[0])
        print('\nError value: \n', e[1]) # contents of .get_build_info LOG
        print('\nError traceback: ', e[2])
        sys.exit()

    return program


if __name__ == '__main__':

    available, devices = discover_devices()

    print('\nOpenCL devices available:')
    for device in devices:
        print('    ', device)

    print('\n')
    print('OpenCL device available? ', 'Yes' if bool(available) else 'No')
