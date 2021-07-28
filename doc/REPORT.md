
## Feature ranking, an early goal for data exploration

Feature ranking, also known as column selection or dimensionality reduction,
is an effort to eliminate "unimportant" features from a set of observations, to 
allow following machine learning steps to focus on "more important" features. 
While domain experts can indicate which features should be dropped from 
consideration, sometimes this task can be automated.

The feature ranking algorithm considered here is the "entropy measure 
for ranking features" technique described in Kantardzic (2011). The idea is that 
observed features will have different degrees of measurable "surprisal" and can 
thus be ranked from least to most important. Kantardzic remarked that this 
algorithm might benefit from parallel computation. It is the goal of this project 
to test the feature ranking algorithm on a widely-available parallel computing 
platform.

This project is a first draft and proof of concept. Only floating point data, 
none missing, is considered here. A more realistic feature ranking scheme would 
include sensitivity to feature types, Hamming distance measures for binary data, 
string-metric measures for character data, and better handling of missing data.

## OpenCL, PyOpenCL, and the OpenCL Programming Language

[OpenCL](https://en.wikipedia.org/wiki/OpenCL) is an industry-supported 
framework (API, interfaces, programming language) to make high-performance 
computing capabilities of CPUS, GPUs, and FPGAs available for data crunching 
under a unified model. HPC devices residing on a workstation can be discovered, 
data can be marshalled, and program "kernels" compiled for execution via OpenCL 
API calls.

PyOpenCL is the OpenCL API "wrapper" for Python. PyOpenCL also hosts a compiler 
for the OpenCL Programming Language. NumPy types in Python are used to marshal 
data into OpenCL devices, and are closely related to the types used in OpenCL 
programming.

The OpenCL Programming Language is a subset of C99, a dialect of C. OpenCL 
problem spaces are generally one-, two- or three-dimensional arrays of data. An 
instance of the kernel, a "work item", executes, in parallel, at every position 
in the problem space. "Work groups" contain work items, and allow for larger
chunks of synchronization and coordination between them.

## Experimental approach

This project implements the entropy measure algorithm once in the NumPy dialect, 
and again in the OpenCL dialect. These implementations are run against each other 
on realistic machine learning datasets, and timing information is presented. A
menu lets a user view and select datasets for trial.

This project also has other supportive stand-alone programs to allow quick
testing, data preparation, and host platform characterization.

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
distance among samples is large. It establishes a pivot point for similarity 
detection.

![equation](https://latex.codecogs.com/svg.image?\alpha&space;=&space;-(ln&space;0.5)&space;/&space;D&space;)

The symbol D is the average distance of samples, and is computationally expensive
to produce because it must evaluate a sum over a (typically) large array, a "reduction" 
step. Parallel processors should be able to speed up this reduction, since additions are 
associative and can be evaluated by "gangs" of adders.

### Similarity measure

The similarity measure, applied to every pairwise comparison, uses the alpha 
parameter to create a very sensitive "switching function" of just which sample 
distances are "surprising" out of the average.

![equation](https://latex.codecogs.com/svg.image?S_i_j&space;=&space;e^{-\alpha&space;D_i_j})

This calculation is prone to parallel speedup because its operations are just
elementwise multiplies and raisings to a power. This is an example of a "mapping"
operation, and is easily implemented in OpenCL.

### Entropy measure

The entropy measure of a dataset, or a feature of a dataset, is a measure of,
in some sense, the amount of "information" or "surprise" or "effort required to
explain" embedded in the data. This measure appears to be flagging, and adding
up, a series of "sweet spots" that are not totally "chaotic" and not totally
"boring", but some place in between.

When feature entropies are compared with each other round-robin, the feature 
with the lowest entropy with respect to the entirety of the dataset is selected 
for removal. This process continues until all features are ranked from the 
"least surprising" to the "most surprising".

![equation](https://latex.codecogs.com/svg.image?E&space;=&space;-\sum_{i=1}^{N-1}&space;\sum_{j=i&plus;1}^{N}(S_i_j&space;*&space;log(S_i_j)&space;&plus;&space;(1-S_i_j)&space;*&space;log(1-S_i_j)))

The evaulation under the sigmas is another case of elementwise arithmetic
operations which can be easily handled in OpenCL. The sigmas introduce another 
big reduction step.

## Data preparation

Five datasets from the UCI Machine Learning Repository were selected to showcase
feature ranking. The datasets are called "wine", "breast", "glass", "german", and
"cardio". More information about them can be found in CREDITS.md.

The criteria for dataset selection is that the they should be of a modest size, 
contain only numeric data (no string or character fields), and have little or
no missing data. Instead of a machine-learning method being selected for use on
data, in this project data was selected for the method! 

The datasets were prepared by deleting columns of "key" or "id" information, 
deleting columns related to target classification, and deleting rows containing
missing data. This project has a framework (prep_data.py) to select a given 
dataset, apply row and column deletions, and present it to the feature ranking 
trial programs. 

In addition, two very small datasets ("simple" and "example") were prepared by 
hand to test and debug feature ranking, and to gain confidence in the way Python
and OpenCL handled sets of data.

## Some results

The "German" and "Cardio" datasets are the largest datasets currently used in 
this project, and present the most challenge to a workstation's capacity to solve 
this problem.

    "German" feature ranking runtimes on some selected platforms. These figures
    will be revisted as improvements are made.

    - Lenovo 7033HH9 Desktop
        CPU: Intel(R) Core(TM) i5-2400 3.10GHz, 4 Logical Processors
            688.74 secs
        GPU: AMD / Cedar
            841.61 secs
        UNACCELERATED (NumPy)
            3279.15 secs

    - Dell Precision 3520 Laptop
        CPU: Intel(R) Core(TM) i7-7700HQ 2.80GHz, 8 Logical Processors
            277.60 secs
        GPU: NVIDIA CUDA / Quadro M620
            317.25 secs
        GPU: Intel(R) OpenCL HD Graphics / Intel(R) HD Graphics 630
            311.93 secs
        UNACCELERATED (NumPy)
            1389.56 secs

    - Dell Precision T5600 Desktop
        CPU: Intel(R) Xeon(R) E5-2603 1.80GHz, 4 Logical Processors
            879.17 secs
        GPU: NVIDIA CUDA / NVS 300 (two installed)
            992.94 secs
        UNACCELERATED (NumPy)
            4734.83 secs

## Lessons learned

Programming in OpenCL has been a challenge for me. Here are some observations.

Data handling comes first. In OpenCL, data must be explicitly moved from main 
memory to HPC device memory, then from device memory to high-speed local memory.
These steps must be explictly reversed to get results back to the host program. 
Actual computations might be as simple as an add or multiply, but positioning 
data is the biggest job.

Data movement also consumes time on the computer's interface bus. This must be 
planned to allow data to reside on the device as long as possible to make the 
best use of time invested in data transfers.

Learning the OpenCL computation model requires some study. The terms "host", 
"problem space", "kernel", "work item", "work group", "compute unit" and "device"
all have definitions and relationships in this model.

A "host" program can be a Python script, and runs on the computer as does any 
other ordinary program. The host program transfers problem data to an HPC "device" 
(such as an on-board GPU), defines the problem space, then calls a kernel. 

A "problem space" is like a matrix or an array of one, two or three dimensions.
A problem space is imposed on the data, the raw data does not carry problem space
information. A "kernel" is a little bit of code, like a small function call. A 
kernel is written in a dialect of C or C++. A kernel that runs at one (x,y,z) 
place in the problem space is called a "work item". 

Many hundreds or thousands of work items run in parallel at their assigned spots 
in the problem space. Groups of work items are collected into chunks called "work 
groups". Work items in a work group can synchronize with each other via the work 
group's local memory and fence/barrier commands. 

Work groups "tile" the problem space, and cannot be synchronized with other work 
groups. When a group of work items complete their tasks, a work group is done. 
When all work groups have run, the entire problem space has been visited and the 
problem is solved. The host program can then collect results.

Work groups are scheduled to run on "compute units" in the HPC device. The device
may have one or more compute units, and work groups can run in any order on any 
available compute unit.

There's a lot more to OpenCL, but these are the basics. Other terms to consider 
are "context" (an object that handles the elements of a complete computation), 
and "queue" (an object that handles commands to a context). OpenCL devices can 
also generate "events". The OpenCL platform also provides a compiler to compile
kernel programs.

An OpenCl developer must learn to think in threads. Computations visit data 
in parallel, so the developer's job is to keep as many work items occupied
as possible. For example, on a single-threaded CPU, a developer might use nested 
loops to visit all of a problem space. Instead, OpenCL will just supply a kernel 
with a couple of variables representing a general position in the problem space. 
The developer learns to trust OpenCL to "unroll" the problem space so they can 
focus on simple, non-conflicting thread action.

Another thing that affects OpenCL performance is branching points (if/else statements).
A branch taken by only one work item might delay the work of thousands of its
fellow work items in its work group, because a work group can only complete when
all its work items complete. Branching points have to be carefully considered,
and possibly factored out and dealt with by cases.

It was helpful to think of OpenCL kernels as a series of mappings, filterings, 
and reductions, so that's why I wrote a first draft of the feature ranking problem 
as a series of Python list comprehensions and NumPy array operations. 

I have found OpenCL kernels difficult to debug, so that's something I need to 
work on. I have managed to hang the GPU on numerous occasions. I have used unsound 
methods and violated the spirit of HPC to get insight into how local memory and 
thread synchronization works. There are kernel profilers available that may help.

    Code refactoring
    - memoize min/max/value_ranges, column extractions, column entropies
    - refactor round-driver code (it's the same body of code)
    - refactor OpenCL context/compile out of round driver
    - set up a configuration scheme

    OpenCL improvements
    - apply reduction methods to min/max (increase thread count)
    - do a better job with sum_array!
    - fix calculation of average (need sum_array to work)
    - fix sum of pairwise entropies (need sum_array to work)
    - on-device sample_distances zero filtering (deal with variable-length arrays)
    - minimize data moves to/from OpenCL devices
    - minimize intermediate work in global memory (global --> local --> global)
    - how to make multi-device execution contexts?
    - how to launch non-blocking kernels?

    Future
    - get execution profile information?
    - look at kernel double-precision floats (cl_khr_fp64 option)
    - find out how to release kernels and buffers in PyOpenCL
    - make the OpenCL and Python host code easier to read, less grindy

## Credits

    Credits and resources can be seen in ./doc/CREDITS.md
