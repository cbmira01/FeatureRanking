
## How to install the feature_reduction project

### Requirements

    - Windows 10
    - At least OpenCL 1.2 HPC devices, either CPU or GPU, discoverable on your workstation
    - Anaconda 2021.05 or a "recent" version
    - a Git client, available at the command line
    - a local directory housing code repositories

### How to setup

    - Open the Anaconda CMD prompt into the Conda (base) environment.

    - Change to your local repository directory:
        cd C:\Users\YourUserName\...\YourLocalRepos>

    - Clone the feature_reduction project GitHub repository:
        git clone https://github.com/cbmira01/feature_reduction

    - Change to the project root directory:
        cd .\feature_reduction

    - Create the Conda environment for the project:
        conda env create --file environment.yml

    - After the environment packages have loaded, activate the new environment:
        conda activate feature_reduction

    - To destroy the feature_reduction project and Conda environment:
        conda deactivate
        conda remove --name feature_reduction --all
        ...then remove all files in the feature_reduction folder, and the folder itself.

### How to run

    - Enumerate OpenCL devices residing on your workstation:
        python discover_devices.py

    - Run simple workloads on your OpenCL devices:
        python simple_workloads.py

    - run the main program:
        python feature_reduction.py


