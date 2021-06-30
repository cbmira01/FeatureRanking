
# Run feature reduction on a given dataset, in the NumPy dialect

import numpy

def run_feature_reduction(dataset):
    return ranked_features
    

# things to do:
#   get a dataset name from calling code
#   if this module is invoked alone, build it's own dataset object
#   how do we run the "example" dataset?
#   needs helpers to:
#       build a dataset object
#       get and parse data.csv
#       get feature names from names.json
#   calculate max and min of each feature in the dataset
#   calculate all Distance[i][j] 
#   calculate D, average of all D[i][j]
#   can we find the ln, log and exp functions?
#   order of calculation (find E for an entire dataset): 
#        max[k], min[k] = maximum, minimum value of feature k
#           max and min are lists over k=1..N of features
#        D[i][j] = (sum{k=1..N}((row[ik] - row[jk]) / (max[k] - min[k])) ** 2) ** 0.5
#        D = average of D[i][j] 
#        alpha = - ln(0.5) / D
#        S[i][j] = exp(-alpha * D[i][j])
#        Entropy measure = 
#           - sum{i=1..N-1}(
#               sum{j=i+1..N}(
#                   (S[i][j] * log(S[i][j]) + (1 - S[i][j]) * log(1 - S[i][j]))
#               )
#             )
#   
# Notes on feature ranking protocol. 
#   Ranking drives the E measure calculation
#   Determines which features to drop from consideration at each stage
#   Step 1:
#   Step 2:
#   Step 3:
#   Step 4:
#   Step 5:
#

