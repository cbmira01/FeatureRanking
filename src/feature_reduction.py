
import json
import sys

def list_datasets():
    print('\n')
    for d in datasets['datasets']:
        print('{}{}'.format(d['short_name'].ljust(10), d['long_name']))
    return None
    
def list_datasets_with_credits():
    for d in datasets['datasets']:
        short_name = d['short_name']        
        credits_file = '../data/' + short_name + '/credit.txt'
        with open(credits_file) as file:
            credit = file.read()
        
        print('\n=======================================================')
        print('{}{}'.format(short_name.ljust(10), d['long_name']), end='')
        print('\n', d['abstract'])
        print('\n', credit)
    return None    

def run_trial():
    print('\nRunning trials...')
    return None

def exit_program():
    print('\nThank you for using feature reduction...')
    sys.exit()
    return None

def switch_on(c):
    switcher = {
        '1': list_datasets,
        '2': list_datasets_with_credits,
        '3': run_trial,
        '4': exit_program
    }
    return switcher.get(c, lambda: 'Invalid')()


# Discover all the available datasets
with open('../data/datasets.json', 'r') as f:
    datasets = json.load(f)

# Main command loop
while True:
    print('\n')
    print('FEATURE REDUCTION main menu')
    print('')
    print('1. List available datasets')
    print('2. List datasets with credits')
    print('3. Run feature reduction trial on a dataset')
    print('4. Exit')
    print('')
    choice = input('Choice? ')
    switch_on(choice)
