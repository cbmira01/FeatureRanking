
#
# This is the main program of the Feature Ranking project.
# It alows the user to list the datasets and choose one for a trial run.
#

import sys
from trial_run import *
from prep_data import *


def list_datasets():
    print('\nDatasets to choose from...\n')
    for ds in datasets_list:
        print('    {}{}'.format(ds['short_name'].ljust(10), ds['long_name']))
    return None


def list_datasets_with_credits():
    for ds in datasets_list:
        short_name = ds['short_name']
        credits_file = '../data/' + short_name + '/credit.txt'
        with open(credits_file) as file:
            credit_text = file.read()

        print('\n========================================================')
        print('{}{}'.format(short_name.ljust(10), ds['long_name']), end='')
        print('\n', ds['abstract'])
        print('\n', credit_text)
    return None


def describe_datasets():
    for ds in datasets_list:
        short_name = ds['short_name']
        print('\n========================================================')
        print('{}{}'.format(short_name.ljust(10), ds['long_name']))
        print('    abstract: ', ds['abstract'])
        print('    website: ', ds['website'])
        print('    instances: ', ds['instances'])
        print('    attributes: ', ds['attributes'])
        print('    remove_attributes: ', ds['remove_attributes'])
        print('    remove_instances: ', ds['remove_instances'])

    return None


def run_a_trial():
    print('\nRun a trial on one of the following datasets: \n')

    for ds in datasets_list:
        print(ds['short_name'], '  ', end='')

    ds_name = input('\n\nPlease chose a dataset name: ').lower()
    ds_info = next((d for d in datasets_list if d['short_name'] == ds_name), None)

    if ds_info is not None:
        run_and_log_trial(ds_info)

    return None


def exit_program():
    print('\nThank you for using feature ranking...')
    sys.exit()
    return None


def switch_on(c):
    switcher = {
        'list': list_datasets,
        'describe': describe_datasets,
        'credits': list_datasets_with_credits,
        'trial': run_a_trial,
        'exit': exit_program
    }
    return switcher.get(c, lambda: 'Invalid')()


datasets_list = discover_datasets()

# Main command loop
while True:
    print('\n')
    print('FEATURE RANKING main menu')
    print()
    print('list ------ List available datasets')
    print('describe -- Describe available datasets')
    print('credits --- List datasets with credits')
    print('trial ----- Run feature ranking trials on a dataset')
    print('exit ------ Exit')
    print()

    switch_on(input('Choice? ').lower())
