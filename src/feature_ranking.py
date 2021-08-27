
#
# This is the main program of the Feature Ranking project.
# It alows the user to list datasets and OpenCL device, and prepare for a trial run.
#

import sys
import trial_runner
from data_handler import *
from device_handler import *


def list_datasets():
 
    print('\nDatasets to choose from...\n')

    for ds in datasets:
        short_name = ds['short_name']
        print('\n========================================================')
        print('{}{}'.format(short_name.ljust(10), ds['long_name']))
        print('    abstract: ', ds['abstract'])
        print('    website: ', ds['website'])
        print('    instances: ', ds['instances'])
        print('    attributes: ', ds['attributes'])
        print('    remove_attributes: ', ds['remove_attributes'])
        print('    remove_instances: ', ds['remove_instances'])

        ic = (instances ** 2 - instances) / 2
        print('    This dataset will require ', ic, ' comparisons bewteen instances')


    # also list number of elementwise comparisons

    return None


def list_devices(dataset_info):

    # for platform in cl.get_platforms():
        # for device in platform.get_devices(cl.device_type.ALL):
            # ranking_protocol(dataset_info, device)

    # return None

    return None


def run_trial():

    # new trial context trial_context = {}

    print('\nRun a trial... \n')

    print('\nChoose a dataset: \n')

    for ds in datasets:
        print(ds['short_name'], '  ', end='')

    ds_name = input('\n\nPlease chose a dataset name: ').lower().strip()
    ds_info = next((d for d in datasets_list if d['short_name'] == ds_name), None)

    if ds_info is not None:
        trial_runner.start(ds_info)

    print('\nChoose an OpenCL device: \n')

    # trial_runner(trial_context)

def exit_program():
    print('\nThank you for using Feature Ranking...')
    sys.exit()
    return None


def switch_on(c.lower().strip()):
    switcher = {
        'datasets': list_datasets,
        'devices': list_devices,
        'trial': zzz,
        'exit': exit_program
    }
    return switcher.get(c, lambda: 'Invalid')()


datasets = discover_datasets()
devices = discover_opencl_devices()

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

    switch_on(input('Choice? '))
