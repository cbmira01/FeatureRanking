
#
# With a given dataset information:
#   - get prepared data
#   - dispatch unacclerated version of Feature Ranking
#   - dispatch OpenCL version of Feature Ranking
#   - collect results and timing information
#   - send some results to the console
#   - log a complete report
#   - return to main program
#
#   - can run stand-alone from the console
#

import sys
from prep_data import *

def run_and_log_trial(dataset_info):
    print('Run and log a trial')
    print(dataset_info)
    results = []

    results.append(dispatch_unaccelerated_fr(dataset_info))
    results.append(dispatch_opencl_fr(dataset_info))

    log_a_report(results)
    return None


def get_prepared_data():
    return None
    
    
def dispatch_unaccelerated_fr(dataset_info):
    print('dispatch unaccel')
    print(dataset_info)
    return None
    
    
def dispatch_opencl_fr(dataset_info):
    print('dispatch opencl')
    print(dataset_info)
    return None
    
    
def log_a_report(results):
    # needs date-time info
    # needs host platform info
    return None


def get_dataset_info_from_name(dataset_name):
    return None


if __name__ == '__main__':

    print('\nCheck trials on console...')

    datasets_list = discover_datasets()

    while True:
        print('\n')
        for ds in datasets_list:
            print(ds['short_name'], '  ', end='')

        ds_name = input('\n\nChoose a dataset: ').lower()
        ds_info = next((d for d in datasets_list if d['short_name'] == ds_name), None)

        trial_choice = input('Workload is \'unaccel\' or \'opencl\': ').lower()

        if trial_choice == 'unaccel' and ds_info is not None:
            dispatch_unaccelerated_fr(ds_info)

        elif trial_choice == 'opencl' and ds_info is not None:
            dispatch_opencl_fr(ds_info)

        else:
            break
    