
#
# This is the main program of the Feature Ranking project.
# It alows the user to list datasets and OpenCL device, and prepare for a trial run.
#

import sys
import math
import trial_runner as tr
import data_handler as dh
import opencl_handler as oh


def list_datasets():
 
    print('\nDatasets to choose from...\n')

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

    devtype_readable = { 
        "1": "DEFAULT",
        "2": "CPU",
        "4": "GPU",
        "8": "ACCELERATOR",
        "16": "CUSTOM",
        }

    print('\nOpenCL devices available...\n')

    if devices_available == False:
        print('No OpenCL devices were discovered on this workstation')
    else:
        for device in devices:
            print('    ', device)
            print('        Processor type: ', devtype_readable.get(str(device.type), "Unknown..."))
            print('        Compute units: ', device.max_compute_units)
            print('        Global memory: ', format(device.global_mem_size, '>1,d'), 'bytes')
            print('        Local memory: ', format(device.local_mem_size, '>1,d'), 'bytes')
            print('        Max work item sizes: ', device.max_work_item_sizes, 'work items')
            print('\n', end='')

    return None


def run_trial():

    print('\nDo feature ranking of a DATASET on a PROCESSOR... \n')
    trial_context = {}

    print('Datasets available:')
    for ds in datasets:
        print('    ', ds['short_name'])

    ds_choice = input('Choose a dataset: ').lower().strip()
    dataset = next((d for d in datasets if d['short_name'] == ds_choice), None)
    if dataset is None:
        return None

    print('\n')
    proc = 0
    print('Processors available:')
    print('    ', proc, ' ---- unaccelerated option')

    for device in devices:
        proc = proc + 1
        print('    ', proc, ' --- ', device)

    processor = int(input('Choose a processor: '))

    if processor not in range(0, proc+1):
        return None

    print(dataset['short_name'], processor)

    # trial_runner(trial_context)
    # trial_runner.start(ds_info)
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


datasets = dh.discover_datasets()
devices_available, devices = oh.discover_devices()

# Main command loop
while True:
    print('\n')
    print('FEATURE RANKING main menu')
    print()
    print('   datasets -- List available datasets')
    print('   devices --- List available OpenCL devices')
    print('   trial ----- Run feature ranking trials on a dataset')
    print('   exit ------ Exit')
    print()

    switch_on(input('Choice? ').lower().strip())
