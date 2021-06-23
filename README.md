
# Feature Reduction

This Python project will qualify the OpenCL framework on a compute-intensive 
data mining task. 

## How to run this project

Refer to requirements and run instructions in INSTRUCTIONS.md

## Feature reduction, an early task in data exploration

Feature reduction, also known as column selection or dimensionality reduction,
is an effort to focus later machine learning steps on the most "important"
features of a set of observations. Sometimes, domain experts can indicate which
features to drop from consideration, and sometimes this task can be automated.

The specific feature reduction algorithm considered here is the "entropy measure"
technique described in Kantardzic (yyyy). The idea is that observed features may
have different degrees of measurable surprisal, or information content, and may 
thus be ranked from most to least important. He remarked that this algorithm might
benefit from parallel computation, and it's the goal of this project to test 
his idea on a widely-available parallel computing platform.

## OpenCL, a high-performance computing framework

OpenCL (...) is an industry-supported framework (API, interfaces, programming 
language) to make the high-performance computing capabilities of CPUS, GPUs,
and FPGAs available for general programming under a unified model. HPC devices
on a workstation can be discovered, data can be marshalled into and out of devices, and 
program "kernels" can be compiled and deployed for execution on devices via OpenCL API calls.

## PyOpenCL, OpenCL hosted in Python

PyOpenCL is the "wrapper" for Python to work with OpenCL, provides Python access to 
the OpenCL API. PyOpenCL also hosts a compiler for the OpenCL Programming Language.
NumPy types in Python are used to marshal data into OpenCL devices, and are closely related
to the types used in OpenCL programming.

## OpenCL Programming Language

The OpenCL Programming Language (OCL), is a subset of C99. OpenCL problem spaces are 
generally one-, two- or three-dimensional arrays of data, and an instance of the
OCL program executes, in parallel, at every node in the problem space. 

## Credits, attributions, works consulted

Credits, attributions, and works consulted are summarized in CREDITS.md.

## Notes for project grading

This project fullfills the following project requirements for Code Louisville:
    - 
