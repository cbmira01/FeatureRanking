
## How to install and run the FeatureReduction project

### Requirements

    - Windows 10
    - At least one OpenCL 1.2 device discoverable on your workstation
    - Anaconda 2021.05 or a "recent" version
    - Git client, available at the command line
    - a local directory on your workstation housing your code repositories

### How to setup

    - Open the Anaconda CMD prompt into the Conda (base) environment.

    - Change to your local repository directory:
        cd C:\Users\YourUserName\...\YourLocalRepos>

    - Clone the FeatureReduction project GitHub repository:
        git clone https://github.com/cbmira01/FeatureReduction

    - Change to the project root directory:
        cd .\FeatureReduction

    - Create the Conda environment for the project:
        conda env create --file environment.yml

    - After the environment packages have loaded, activate the new Conda environment:
        conda activate feature_reduction

    - To destroy the feature_reduction project and Conda environment:
        conda deactivate
        conda remove --name feature_reduction --all
        ...then remove the FeatureReduction folder and its contents.

### How to run

    - Discover OpenCL devices residing on your workstation:
        python discover_devices.py

    - Run simple workloads on your OpenCL devices:
        python simple_workloads.py

    - run the main program:
        python feature_reduction.py
