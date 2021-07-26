
## How to install and run the FeatureRanking project

### Requirements

    This project was built and tested on Windows 10 64-bit, with up-to-date 
    CPU and GPU drivers. You'll need at least one OpenCL device discoverable on 
    your workstation, a "recent" version of Anaconda (eg, 2021.05), a Git 
    client like [Git Bash](https://git-scm.com) available at the Anaconda command 
    line, and a local directory on your workstation where your code repositories
    are housed.

### Setup from scratch

    - Open the Anaconda CMD prompt into the Conda (base) environment.

    - Change to your preferred local repository base directory:
          cd C:\Users\your-user-name\...\your-local-repos>

    - Clone the FeatureRanking project GitHub repository:
          git clone https://github.com/cbmira01/FeatureRanking

    - Change to the FeatureRanking project root directory:
          cd .\FeatureRanking

    - Create the Conda environment for the project:
          conda env create --file environment.yml

    - After packages have loaded, activate the new Conda environment:
          conda activate feature_ranking

### Test the installation

    - To run Python programs, change to the .\src folder:
        cd .\src

    - The quick test program will dump a list of available OpenCL devices,
      and run a very small OpenCL workload on each one:
          python quick_test.py

### After a successful installation

    - Run the main program:
          python feature_ranking.py

### Return to previously installed project

    - Open the Anaconda CMD prompt into the Conda (base) environment.

    - Change to the FeatureRanking project root directory:
          cd C:\Users\your-user-name\...\your-local-repos\FeatureRanking

    - Activate the existing Conda environment:
          conda activate feature_ranking

### Update environment packages

    - To update environment packages after repository changes, change to the
      FeatureRanking project root directory, then:
        git pull
        conda env update --name feature_ranking --file environment.yml

### Destroy the environment and project

    - To destroy the feature_ranking Conda environment:
        conda deactivate
        conda remove --name feature_ranking --all

    - To destroy the FeatureRanking project entirely, first destroy the
      feature_ranking environment, then remove the FeatureRanking folder
      and its contents.

### If you have difficulty...
    
    I have tested this project on five workstations of various vintages, and have
    always managed to either find or establish an OpenCL device. On a Lenovo
    T400 (circa 2008), while I found no GPU device, I did discover that the CPU
    was rated as an available OpenCL device. Any computer presenting an OpenCL
    device should be able to run this project.

    Unfortunately, installing PyOpenCL on Windows is still more an art than a 
    science. If you encounter difficulty running the quick test, you may need a 
    pip 'wheel' (pre-compiled binary) that supports older OpenCL device drivers. 
    Here's how to do it...

    - Visit [Pre-compiled OpenCL binaries](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopencl)

    - Download a wheel appropriate for your OpenCL version, vendor type, and 
      Python version. For example, for PyOpenCL 2021.2.2, Python 3.9, and OpenCL 
      version 1.2, try one of the following wheels:
          pyopencl-2021.2.2+cl12-cp39-cp39-win_amd64.whl
          pyopencl-2021.2.2+cl12-cp39-cp39-win32.whl

    - Install the wheel. This action will replace the Conda package version
      of PyOpenCL. Make sure the feature_ranking environment is still
      activated, and that you are positioned in FeatureRanking project root:
          pip install C:\Users\your-user-name\...\Downloads\<wheel-name>.whl

    - Try the quick test again. If you still see problems, try other pip wheels 
      as appropriate. It is also possible that you are experiencing driver 
      problems, or that you may have no discoverable OpenCL devices on your 
      workstation.

    - I have found the "AMD Accelerated Parallel Processing SDK" (AMD APP SDK)
      can allow an Intel CPU to be recognized as an OpenCL devices. This may be 
      worth investigating if your workstation does not have a GPU. 
      See these links:
          [AMD APP SDK](https://en.wikipedia.org/wiki/AMD_APP_SDK)
          [AMD APP SDK discussion](https://github.com/fireice-uk/xmr-stak/issues/1511)
