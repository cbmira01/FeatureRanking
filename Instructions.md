
## How to install and run the FeatureReduction project

### Requirements

    - Windows 10 with most up-to-date CPU and GPU drivers
    
    - at least one OpenCL device discoverable on your workstation
    
    - Anaconda 2021.05 or a "recent" version
    
    - Git client, available at the command line
    
    - a local directory on your workstation housing your code repositories

### How to setup

    - Open the Anaconda CMD prompt into the Conda (base) environment.

    - Change to your local repository directory:
          cd C:\Users\YourUserName\...\YourLocalRepos>

    - Clone the FeatureReduction project GitHub repository:
          git clone https://github.com/cbmira01/FeatureReduction

    - Change to the FeatureReduction project root directory:
          cd .\FeatureReduction

    - Create the Conda environment for the project:
          conda env create --file environment.yml

    - After the environment packages have loaded, activate the new Conda environment:
          conda activate feature_reduction

    - When you want to destroy the feature_reduction environment:
          conda deactivate
          conda remove --name feature_reduction --all
          ...then remove the FeatureReduction folder and its contents.

### Test the installation

    - The quick test program will dump a list of available OpenCL devices,
      and run a very small OpenCL workload on each one:
          python quick_test.py

### If you have difficulty...

    Unfortunately, installing PyOpenCL on Windows is still more an art
    than a science. If you encounter difficulty running the quick test, 
    you may need a pip 'wheel' (pre-compiled binary) that supports older
    OpenCL device drivers. Here's how to do it:
    
    - Visit http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopencl 
    
    - Download a wheel appropriate for the OpenCL driver level, vendor 
      type, and Python version. For example, for the most recent version
      of PyOpenCL, Python 3.9, and OpenCL driver level 1.2, try one of
      the following wheels:
          pyopencl-2021.2.2+cl12-cp39-cp39-win_amd64.whl
          pyopencl-2021.2.2+cl12-cp39-cp39-win32.whl
        
    - Install the wheel. This action will replace the Conda package version
      of PyOpenCL. Make sure the feature_reduction environment is still
      activated, and that you are positioned in FeatureReduction project root:
          pip install C:\Users\YourUserName\Downloads\<wheelname>.whl
    
    - Try the quick test again. If you still see problems, try other pip 
      wheels as appropriate. It is also possible that you are experiencing 
      driver problems, or that you may have no discoverable OpenCL devices
      on your workstation.
    
### After a successful installation

    - Run simple workloads on your OpenCL devices:
          python simple_workloads.py

    - run the main program:
          python feature_reduction.py

