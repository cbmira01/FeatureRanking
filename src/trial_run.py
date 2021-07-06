
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

def run_and_log_trial(dataset_info):
    print('Run and log a trial')
    print(dataset_info)
    results = get_prepared_data()
    results = dispatch_unaccelerated_fr()
    results = dispatch_opencl_fr()
    log_a_report()
    return None


def get_prepared_data():
    return None
    
    
def dispatch_unaccelerated_fr():
    return None
    
    
def dispatch_opencl_fr():
    return None
    
    
def log_a_report():
    # needs date-time info
    # needs host platform info
    return None


def get_dataset_info_from_name(dataset_name):
    return None


if __name__ == '__main__':
    sys.exit()
