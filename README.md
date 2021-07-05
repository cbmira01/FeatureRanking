
# Feature Reduction

This Python project will implement a compute-intensive data mining task in 
workstation devices capable of parallel computation. A particular data science 
algorithm for feature reduction is implemented in the OpenCL framework, and 
compared to an unaccelerated version.

## How to run this project

Requirements, setup and run instructions are described in 
<p align="center">./doc/INSTRUCTIONS.md</p> 

## Feature reduction, an early goal for data exploration

Feature reduction, also known as column selection or dimensionality reduction,
is an effort to eliminate "unimportant" features from a set of observations, to 
allow following machine learning steps to focus on "more important" features. 
While domain experts can indicate which features should be dropped from 
consideration, sometimes this task can be automated.

The specific feature reduction algorithm considered here is the "entropy measure 
for ranking features" technique described in Kantardzic (2011). The idea is that 
observed features will have different degrees of measurable "surprisal" and can 
thus be ranked from most to least important. Kantardzic remarked that this 
algorithm might benefit from parallel computation. It is the goal of this project 
to test this algorithm on a widely-available parallel computing platform.

This project is a first draft and proof of concept. Only floating point data, 
none missing, is considered here. A more realistic feature reduction scheme would 
include sensitivity to feature types, Hamming distance measures for binary data, 
string-metric measures for character data, and better handling of missing data.

## OpenCL, a high-performance computing framework

OpenCL (https://en.wikipedia.org/wiki/OpenCL) is an industry-supported 
framework (API, interfaces, programming language) to make high-performance 
computing capabilities of CPUS, GPUs, and FPGAs available for data crunching 
under a unified model. HPC devices residing on a workstation can be discovered, 
data can be marshalled, and program "kernels" compiled for execution via OpenCL 
API calls.

## PyOpenCL, OpenCL hosted in Python

PyOpenCL is the "wrapper" for Python to access the OpenCL API. PyOpenCL also 
hosts a compiler for the OpenCL Programming Language. NumPy types in Python 
are used to marshal data into OpenCL devices, and are closely related to the 
types used in OpenCL programming.

## OpenCL Programming Language

The OpenCL Programming Language is a subset of C99, a dialect of C. OpenCL 
problem spaces are generally one-, two- or three-dimensional arrays of data. An 
instance of the kernel executes, in parallel, at every position in the problem 
space.

## Experimental approach of this project

This project will:

    - Implement the entropy measure algorithm in the NumPy dialect.
      This code will run on the machine's CPU as an unaccelerated workload.

    - Implement the entropy measure algorithm again in the OpenCL dialect.
      This code will run on discoverable HPC devices as a parallel computation. 

    - Run the NumPy and OpenCL implementations against each other on realistic 
      machine learning datasets. It is possible to add more datasets.

    - Run the OpenCL workload on all discoverable, or selected, HPC devices.

    - Log timing information for each run.

    - Provide menus to allow user interaction.

This project also has other supportive stand-alone programs to allow quick
testing, host platform characterization, and running small OpenCL workloads. 

The goals of this project are to qualify OpenCL as a suitable platform for data 
science software, to provide a well-constructed example of OpenCL programming 
hosted in Python, and to learn how to use high-performace resources on ordinary 
workstations.

Notes on the equations used to develop the feature reduction algorithm are in
doc\NOTES.md. I hope to post some results of these experiments in doc\RESULTS.md.

## Credits, attributions, works consulted

Credits, attributions, and works consulted are summarized in doc\CREDITS.md.

## Notes for project grading

This project fullfills the following project requirements for Code Louisville:

    - feature 1

    - feature 2

    - feature 3

    - feature 4
