
#
# This is the main program of the Feature Ranking project.
# It allows the user to list datasets and OpenCL devices, and prepare for a trial run.
#

import sys
import math
import trial_runner as tr
import data_handler as dh
import opencl_handler as oh


def list_datasets():
 
    print('\nDatasets to choose from...\n')
    datasets = dh.discover_datasets()

    for ds in datasets:
        short_name = ds['short_name']
        instances = ds['instances'] - len(ds['remove_instances'])
        attributes = ds['attributes'] - len(ds['remove_attributes'])
        comparisons = math.floor((instances ** 2 - instances) / 2)

        print('{}{}'.format(short_name.ljust(10), ds['long_name']))
        print('    abstract: ', ds['abstract'])
        print('    website: ', ds['website'])
        print('    clean instances: ', instances, '    clean attributes: ', attributes)
        print('        This dataset will require ', comparisons, ' comparisons between instances')
        print('\n', end='')

    return None


def list_devices():

    print('\nOpenCL devices available...\n')
    device_type = oh.devtype_readable
    devices = oh.discover_devices()

    if not devices:
        print('No OpenCL devices were discovered on this workstation')
    else:
        for device in devices:
            print('    ', device)
            print('        Processor type: ', device_type.get(str(device.type), "Unknown..."))
            print('        Compute units: ', device.max_compute_units)
            print('        Global memory: ', format(device.global_mem_size, '>1,d'), 'bytes')
            print('        Local memory: ', format(device.local_mem_size, '>1,d'), 'bytes')
            print('        Max work item sizes: ', device.max_work_item_sizes)
            print('\n', end='')

    return None


def run_trial():

    print('\nPerform feature ranking of a DATASET on a computing DEVICE...')
    datasets = dh.discover_datasets()
    devices = oh.discover_devices()
    log_results = False

    print('\nDatasets available:')
    for ds in datasets:
        print('    ', ds['short_name'])

    ds_choice = input('Choose a dataset: ').lower().strip()
    dataset = next((d for d in datasets if d['short_name'] == ds_choice), None)
    if dataset is None:
        return None

    print('\nDevices available:')
    print('    ', 0, ' ---- unaccelerated option')
    for idx, device in enumerate(devices):
        print('    ', idx+1, ' --- ', device)

    dvc = input('Choose a device: ')
    try:
       int(dvc)
    except ValueError:
       return None
    
    dv_choice = int(dvc)
    if dv_choice not in range(0, len(devices) + 1):
        return None

    if dv_choice == 0:
        device = None
        device_name = 'unaccelerated CPU'
    else:
        device = devices[dv_choice - 1]
        device_name = device.name.lstrip()

    log_choice = input('Log results? Yes/No: ').lower().strip()
    if log_choice == 'yes':
        log_results = True

    trial_context = {
        "dataset": dataset,
        "device": device,
        "device_name": device_name,
        "log_results": log_results
    }
    tr.start(trial_context)

    return None


def exit_program():
    print('\nThank you for using Feature Ranking...')
    sys.exit()
    return None


def switch_on(c):
    switcher = {
        'datasets': list_datasets,
        'devices': list_devices,
        'trial': run_trial,
        'exit': exit_program
    }
    return switcher.get(c, lambda: 'Invalid')()


# Main command loop
while True:
    print('\n')
    print('FEATURE RANKING main menu')
    print()
    print('   datasets -- List available datasets')
    print('   devices --- List available OpenCL devices')
    print('   trial ----- Run a feature ranking trial on a dataset')
    print('   exit ------ Exit')
    print()

    switch_on(input('Choice? ').lower().strip())
