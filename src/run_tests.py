
import numpy as np
import unaccelerated as unacc
import accelerated as acc


# for k in range(features):
    # fc[k] = [[c] for c in columns[k]]

# for k in range(features):
    # print(fc[k])

def test_feature_entropies(dataset):
    columns = np.array(dataset).transpose().tolist()
    fe_list = []
    for k in range(0, 5):
        fe_list.append(unacc.get_entropy([[c] for c in columns[k]]))
    return fe_list

def test_dataset_entropy(dataset):
    return unacc.get_entropy(dataset)

def compare_close_lists(a, b):
    if len(a) != len(b):
        return False
    else:
        test = True
        for av, bv in zip(a, b):
            if not np.isclose(av, bv):
                test = False
                break
    return test


if __name__ == '__main__':

    dataset = [
        [0.34818205,0.0054406016,0.17633587,0.010881203,2.5290077],
        [0.9478498,0.8079211,0.9687416,1.6158422,4.9062247],
        [0.2887636,0.450703,0.29179972,0.901406,2.875399],
        [0.62086165,0.59616053,0.09807767,1.1923211,2.294233],
        [0.017327862,0.823534,0.6032455,1.647068,3.8097365],
        [0.06374773,0.86418086,0.9055053,1.7283617,4.716516],
        [0.33667052,0.23504795,0.6865279,0.4700959,4.0595837],
        [0.82834285,0.35440725,0.123982616,0.7088145,2.3719478],
        [0.92590517,0.41533554,0.62911564,0.8306711,3.887347],
        [0.5316418,0.52066636,0.3490727,1.0413327,3.047218]
    ]

    print('\n\nTesting unaccelerated functions...\n')

    feu_should_be = [11.33802962663634, 11.34964269530792, 11.266012823645426, 11.349642672172035, 11.266012701437333]
    feu = test_feature_entropies(dataset)
    print('Feature entropies, unaccelerated...')
    print('  feu:           ', feu)
    print('  feu_should_be: ', feu_should_be)
    print('      Succeeded' if compare_close_lists(feu, feu_should_be) else '    FAILED')
    print()
    
    dseu_should_be = 12.88915033483721
    dseu = test_dataset_entropy(dataset)
    print('Dataset entropy, unaccelerated...')
    print('  dseu:           ', dseu)
    print('  dseu_should_be: ', dseu_should_be)
    print('      Succeeded' if np.isclose(dseu, dseu_should_be) else '    FAILED')
    print()

    # if an OpenCL device is found, do the same tests on the accelerated platform
