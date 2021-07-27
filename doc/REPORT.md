
## Feature ranking, an early goal for data exploration

Feature ranking, also known as column selection or dimensionality reduction,
is an effort to eliminate "unimportant" features from a set of observations, to 
allow following machine learning steps to focus on "more important" features. 
While domain experts can indicate which features should be dropped from 
consideration, sometimes this task can be automated.

The feature ranking algorithm considered here is the "entropy measure 
for ranking features" technique described in Kantardzic (2011). The idea is that 
observed features will have different degrees of measurable "surprisal" and can 
thus be ranked from most to least important. Kantardzic remarked that this 
algorithm might benefit from parallel computation. It is the goal of this project 
to test this algorithm on a widely-available parallel computing platform.

This project is a first draft and proof of concept. Only floating point data, 
none missing, is considered here. A more realistic feature ranking scheme would 
include sensitivity to feature types, Hamming distance measures for binary data, 
string-metric measures for character data, and better handling of missing data.

## OpenCL, PyOpenCL, and the OpenCL Programming Language

OpenCL (https://en.wikipedia.org/wiki/OpenCL) is an industry-supported 
framework (API, interfaces, programming language) to make high-performance 
computing capabilities of CPUS, GPUs, and FPGAs available for data crunching 
under a unified model. HPC devices residing on a workstation can be discovered, 
data can be marshalled, and program "kernels" compiled for execution via OpenCL 
API calls.

PyOpenCL is the "wrapper" for Python to access the OpenCL API. PyOpenCL also 
hosts a compiler for the OpenCL Programming Language. NumPy types in Python 
are used to marshal data into OpenCL devices, and are closely related to the 
types used in OpenCL programming.

The OpenCL Programming Language is a subset of C99, a dialect of C. OpenCL 
problem spaces are generally one-, two- or three-dimensional arrays of data. An 
instance of the kernel executes, in parallel, at every position in the problem 
space.

## Experimental approach

This project implements the entropy measure algorithm once in the NumPy dialect, 
and again in the OpenCL dialect. These implementations are run against each other 
on realistic machine learning datasets, and timing information is presented. A
menu lets a user view and select datasets for trial.

This project also has other supportive stand-alone programs to allow quick
testing, and host platform characterization.

The goals of this project are to qualify OpenCL as a suitable platform for data 
science software, to provide a well-constructed example of OpenCL programming 
hosted in Python, and to learn how to use high-performace resources on ordinary 
workstations.

## Governing equations

### Distance between samples

In some sense, dataset samples are "similar" to each other if they are "near" to
each other. The Euclidean metric is one way to establish "distance" between features.
Hamming distance or string distance metrics are other ways to establish distances.

![equation](https://latex.codecogs.com/svg.image?D_i_j&space;=&space;\left&space;[&space;\sum_{k=1}^{n}&space;((x_i_k&space;-&space;x_j_k)&space;/&space;(max_k&space;-&space;min_k))^{2}&space;\right&space;]^{1/2})

This step is computationally expensive in that it creates an upper-triangular 
structure from the matrix of pair-wise comparisons. For 10 dataset samples, 
45 comparisons are created; 100 samples would create nearly 5000 comparisons; 
1000 samples (as in the "German" dataset) create nealy a half-million comparisons.
And the "Cardio" dataset, at 2126 samples, creates well over two million 
comparisons. This step is greatly aided by parallel computation.

### Alpha parameter

The alpha parameter is a sort of "learning" parameter, because it is influenced 
by all the samples in the dataset. It acts as a "magnifier" for datasets that 
have small average distances, and a "flattener" for datasets where the average 
distance among samples is large. 

![equation](https://latex.codecogs.com/svg.image?\alpha&space;=&space;-(ln&space;0.5)&space;/&space;D&space;)

The symbol D is the average distance of samples, and is computationally expensive
in that it must evaluate a sum over a (typically) large array, a "reduction" step. 
Parallel processors should be able to speed up this reduction, since additions are 
associative and can be evaluated by "gangs" of adders.

### Similarity measure

The similarity measure, by factoring in the alpha parameter, tries to be a very
sensitive "switching function" of just which sample distances are "surprising"
out of the average. 

![equation](https://latex.codecogs.com/svg.image?S_i_j&space;=&space;e^{-\alpha&space;D_i_j})

This calculation is prone to parallel speedup because its operations are just
elementwise multiplies and raisings to a power. This is an example of a "mapping"
operation, and is easily implemented in OpenCL.

### Entropy measure

The entropy measure of a dataset, or a feature of a dataset, is a measure of,
in some sense, the amount of "information" or "surprise" or "effort required to
explain" embedded in the data. When features are compared with each other 
round-robin, the feature with the lowest entropy with respect to the entirety of
the dataset is selected for removal. This process continues until all features 
are ranked from the "least surprising" to the most.

![equation](https://latex.codecogs.com/svg.image?E&space;=&space;-\sum_{i=1}^{N-1}&space;\sum_{j=i&plus;1}^{N}(S_i_j&space;*&space;log(S_i_j)&space;&plus;&space;(1-S_i_j)&space;*&space;log(1-S_i_j)))

The evaulation under the sigmas is another case of elementwise arithmetic
operations which can be easily handled in OpenCL. The sigmas introduce another 
big reduction step.

## Some results

The "Cardio" dataset is the largest dataset currently used in this project, and
is the most stringent test of a workstation's computing capacity to solve this 
problem. Presented are some trial run timings.

Work in progress... "Cardio" runtimes on devices...

- Lenovo 7033HH9
  Intel(R) Core(TM) i5-2400 CPU @ 3.10GHz, 3101 Mhz, 4 Cores

- Dell laptop

- Dell desktop

## Lessons learned

Work in progress...

- memoize min/max/value_ranges
- do a better job with sum_array!
- do a better job with sample_distances zero filtering
- fix calculation of average (need sum_array to work)
- fix sum of pairwise entropies (need sum_array to work)
- refactor round-driver code (needs to be in common)
- refactor OpenCL context/compile out of round driver
- minimize data moves to/from OpenCL devices
- minimize intermediate work in global memory (global --> local --> global)
- find out how to release kernels and buffers in PyOpenCL
- make the OpenCL and Python host code easier to read, less grindy

## Credits

Credits and resources can be seen in ./doc/CREDITS.md
