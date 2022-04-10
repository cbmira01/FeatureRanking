
#
# The trial runner looks at the trial context, then runs the ranking protocol.
#
# A trial context knows about the chosen dataset and the chosen processor type.
#

import time
import numpy as np
import unaccelerated as unacc
import accelerated as acc
import data_handler as dh
import opencl_handler as oh
import sys


def start(trial_context):

    dataset_info = trial_context["dataset"]
    dataset = dh.get_clean_data(dataset_info, dump=False)
    labels = dh.get_label_names(trial_context["dataset"])
    device = trial_context["device"]
    device_name = trial_context["device_name"]

    print('\nRanking trial of \"', dataset_info['long_name'], '\"', end='')
    print(' on ', device_name)
    
    if (False): # configuration
        print('Label names: ', labels)

    if device:
        is_accelerated = True
        context = oh.get_context(device)
        program = oh.build_opencl_program(context)
    else:
        is_accelerated = False

    # The ranking protocol will rank dataset features from the "least important"
    #   to the "most important", in the sense that low-ranking features
    #   contribute the least "surprisal" to the remaining dataset to which they
    #   being compared. In each round, the protocol will identify the least
    #   contributing feature, then drop it from consideration in following
    #   rounds.

    # Step 1a: Start with an initial full set of features (no exclusions).
    instances = len(dataset)
    features = len(dataset[0])
    exclude = [False for k in range(features)]
    counter = 1

    ranking_start = time.perf_counter()

    # Step 1b: Do precomputations on min/max/value ranges
    # Step 1c: Do feature entropy precomputations

    while True:
        # Step 2a: Find the total entropy of the remaing dataset.
        remaining_dataset = []
        for row in dataset:
            remaining_dataset.append([row[k] for k in range(features) if not exclude[k]])

        if is_accelerated:
            remaining_entropy = acc.get_entropy(remaining_dataset, context, program)
        else: 
            remaining_entropy = unacc.get_entropy(remaining_dataset)

        # Step 2b: Find the entropies of each non-excluded feature.
        columns = np.array(dataset).transpose().tolist()
        feature_entropies = [] # for debugging
        entropy_differences = []

        for k in range(features):
            if exclude[k]:
                feature_entropies.append(None)
                entropy_differences.append(float('inf')) # force no test here
            else:
                if is_accelerated:
                    feature_entropy = acc.get_entropy([[c] for c in columns[k]], context, program)
                else:
                    feature_entropy = unacc.get_entropy([[c] for c in columns[k]])

                feature_entropies.append(feature_entropy)
                entropy_difference = np.absolute(np.subtract(remaining_entropy, feature_entropy))
                entropy_differences.append(entropy_difference)

        # Step 3: Find the feature fk such that the difference between the
        #   total entropy and feature entropy for fk is minimum.
        drop_index = entropy_differences.index(min(entropy_differences))

        # Step 4: Exclude feature fk from the dataset and report it as the
        #   "least contributing" feature.
        exclude[drop_index] = True

        print('   Round ', counter, '-  dropped feature  ', labels[drop_index], end='')
        print(',  remaining entropy', remaining_entropy)
        if (False): # configuration
            print('    Entropy differences: ', entropy_differences)
        sys.stdout.flush() 

        # Step 5: Repeat steps 2–4 until no features remain.
        counter = counter + 1
        if exclude.count(False) == 0:
            break

    ranking_stop = time.perf_counter()
    print(f"Ranking completed in {ranking_stop - ranking_start:0.2f} seconds")

    return None
