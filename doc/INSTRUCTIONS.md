
## How to install and run the FeatureReduction project

### Requirements

    - Windows 10 64-bit, with most up-to-date CPU and GPU drivers

    - at least one OpenCL device discoverable on your workstation

    - Anaconda 2021.05 or a "recent" version

    - Git client, available at the Anaconda command line

    - a local directory on your workstation housing your code repositories

### Setup from scratch

    - Open the Anaconda CMD prompt into the Conda (base) environment.

    - Change to your preferred local repository base directory:
          cd C:\Users\your-user-name\...\your-local-repos>

    - Clone the FeatureReduction project GitHub repository:
          git clone https://github.com/cbmira01/FeatureReduction

    - Change to the FeatureReduction project root directory:
          cd .\FeatureReduction

    - Create the Conda environment for the project:
          conda env create --file environment.yml

    - After packages have loaded, activate the new Conda environment:
          conda activate feature_reduction

### Return to previously installed project

    - Open the Anaconda CMD prompt into the Conda (base) environment.

    - Change to the FeatureReduction project root directory:
          cd C:\Users\your-user-name\...\your-local-repos\FeatureReduction

    - Activate the existing Conda environment:
          conda activate feature_reduction

### Update environment packages

    - To update environment packages after repository changes, change to the
      FeatureReduction project root directory, then:
        git pull
        conda env update --name feature_reduction --file environment.yml

### Destroy the environment and project

    - To destroy the feature_reduction Conda environment:
        conda deactivate
        conda remove --name feature_reduction --all

    - To destroy the FeatureReduction project entirely, first destroy the
      feature_reduction environment, then remove the FeatureReduction folder
      and its contents.

### Test the installation

    - To run the python programs, change to the .\src folder:
        cd .\src

    - The quick test program will dump a list of available OpenCL devices,
      and run a very small OpenCL workload on each one:
          python quick_test.py

    - The host information program will dump information about your workstation:
          python host_info_full.py
          python host_info_brief.py

### If you have difficulty...

    Unfortunately, installing PyOpenCL on Windows is still more an art than a 
    science. If you encounter difficulty running the quick test, you may need a 
    pip 'wheel' (pre-compiled binary) that supports older OpenCL device drivers. 
    Here's how to do it...

    - Visit http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopencl

    - Download a wheel appropriate for your OpenCL version, vendor type, and 
      Python version. For example, for PyOpenCL 2021.2.2, Python 3.9, and OpenCL 
      version 1.2, try one of the following wheels:
          pyopencl-2021.2.2+cl12-cp39-cp39-win_amd64.whl
          pyopencl-2021.2.2+cl12-cp39-cp39-win32.whl

    - Install the wheel. This action will replace the Conda package version
      of PyOpenCL. Make sure the feature_reduction environment is still
      activated, and that you are positioned in FeatureReduction project root:
          pip install C:\Users\your-user-name\...\Downloads\<wheel-name>.whl

    - Try the quick test again. If you still see problems, try other pip wheels 
      as appropriate. It is also possible that you are experiencing driver 
      problems, or that you may have no discoverable OpenCL devices on your 
      workstation.

    - I have found the "AMD Accelerated Parallel Processing SDK" (AMD APP SDK)
      can allow Intel CPUs to be recognized as OpenCL devices. This may be worth
      investigating if your workstation does not have a GPU. See these links:
          https://en.wikipedia.org/wiki/AMD_APP_SDK
          https://github.com/fireice-uk/xmr-stak/issues/1511

### After a successful installation

    - Run simple workloads on your OpenCL devices:
          python simple_workloads.py

    - run the main program:
          python feature_reduction.py
