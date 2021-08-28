
#
# The trial runner looks at the trial context, then runs the ranking protocol.
#
# A trial context knows about the chosen dataset and the chosen processor type.
#

import time
import unaccelerated as unacc
import accelerated as acc
import data_handler as dh
import opencl_handler as oh


def start(trial_context):


    if ds_info is not None:
        unaccelerated.rank(ds_info)
        accelerated.rank(ds_info)

    # TODO:
    #       - get cleaned data
    #       - if the processor type is OpenCL, get an OCL context and build the kernels
    #       - run and time the ranking protocol





    return None


def build_kernels():
    # Prepare the OpenCl context, command queue and program for the current device
    # context = cl.Context([device])

    # try: 
        # with open('./kernels/feature_ranking.cl', 'r') as f:
            # kernel_source = f.read()

        # program = cl.Program(context, kernel_source).build()
    # except:
        # print('\n\n      There was an error while building the kernel...')
        # e = sys.exc_info()
        # print('\nError type: ', e[0])
        # print('\nError value: \n', e[1]) # contents of .get_build_info LOG
        print('\nError traceback: ', e[2])
        # sys.exit()


def ranking_protocol(dataset_info, device):

    # The ranking protocol will rank dataset features from the "least important"
    #   to the "most important", in the sense that low-ranking features
    #   contribute the least "surprisal" to the remaining dataset to which they
    #   being compared. In each round, the protocol will identify the least
    #   contributing feature, then drop it from consideration in following
    #   rounds.

    # dataset = get_clean_data(dataset_info, dump=False)
    # label_names = get_label_names(dataset_info)

    # print('\n')
    # print('Trial on OpenCL device: ', device)
    # print('Dataset: ', dataset_info['long_name'])
    # if (False): # configuration
        # print('Label names: ', label_names)

    ranking_start = time.perf_counter()

    # Step 1a: Start with an initial full set of features (no exclusions).
    instances = len(dataset)
    features = len(dataset[0])
    exclude = [False for k in range(features)]
    counter = 1

    # Step 1b: Do precomputations on min/max/value ranges
    # Step 1c: Do feature enropy precomputations

    while True:
        # Step 2a: Find the total entropy of the remaing dataset.
        remaining_dataset = []
        for row in dataset:
            remaining_dataset.append([row[k] for k in range(features) if not exclude[k]])

        remaining_entropy = get_entropy_opencl(remaining_dataset, context, program)

        # Step 2b: Find the entropies of each non-excluded feature.
        columns = np.array(dataset).transpose().tolist()
        feature_entropies = [] # for debugging
        entropy_differences = []

        for k in range(features):
            if exclude[k]:
                feature_entropies.append(None)
                entropy_differences.append(float('inf')) # force no test here
            else:
                fe = get_entropy_opencl([[c] for c in columns[k]], context, program)
                feature_entropies.append(fe)
                ed = np.absolute(np.subtract(remaining_entropy, fe))
                entropy_differences.append(ed)

        # Step 3: Find the feature fk such that the difference between the
        #   total entropy and feature entropy for fk is minimum.
        drop_index = entropy_differences.index(min(entropy_differences))

        # Step 4: Exclude feature fk from the dataset and report it as the
        #   "least contributing" feature.
        exclude[drop_index] = True

        print('   Round', counter, ', dropped', label_names[drop_index], end='')
        print(', remaining entropy', remaining_entropy)
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
