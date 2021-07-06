
import sys
import trial_run as trial
import prep_data as prep


def list_datasets():
    print('\n')
    for ds in datasets_list:
        print('{}{}'.format(ds['short_name'].ljust(10), ds['long_name']))
    return None


def list_datasets_with_credits():
    for ds in datasets_list:
        short_name = ds['short_name']
        credits_file = '../data/' + short_name + '/credit.txt'
        with open(credits_file) as file:
            credit_text = file.read()

        print('\n=======================================================')
        print('{}{}'.format(short_name.ljust(10), ds['long_name']), end='')
        print('\n', ds['abstract'])
        print('\n', credit_text)
    return None


def run_a_trial():
    print('\nRun a trial on one of the following datasets: \n')

    for ds in datasets_list:
        print(ds['short_name'], '  ', end='')

    ds_name = input('\n\nPlease chose a dataset name: ').lower()
    ds_chosen = next((d for d in datasets_list if d['short_name'] == ds_name), None)

    if ds_chosen is not None:
        trial.run_and_log_trial(ds_chosen)

    return None


def exit_program():
    print('\nThank you for using feature ranking...')
    sys.exit()
    return None


def switch_on(c):
    switcher = {
        'list': list_datasets,
        'credits': list_datasets_with_credits,
        'trial': run_a_trial,
        'exit': exit_program
    }
    return switcher.get(c, lambda: 'Invalid')()


datasets_list = prep.discover_datasets()

# Main command loop
while True:
    print('\n')
    print('FEATURE RANKINGS main menu')
    print()
    print('list ---- List available datasets')
    print('credits - List datasets with credits')
    print('trial --- Run feature ranking trial on a dataset')
    print('exit ---- Exit')
    print()
    choice = input('Choice? ').lower()
    switch_on(choice)
