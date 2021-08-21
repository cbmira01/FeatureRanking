
# Feature Ranking

This Python project implements a compute-intensive data mining task on 
workstation devices capable of parallel computation. A particular data science 
algorithm for feature ranking is implemented in the OpenCL framework and 
compared to an unaccelerated version written in Python (NumPy).

## How to run this project

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
    > cd C:\\Users\\your-user-name\\...\\your-local-repos>

- Clone the FeatureRanking project GitHub repository: 
    > git clone https://github.com/cbmira01/FeatureRanking

- Change to the FeatureRanking project root directory: 
    > cd .\FeatureRanking

- Create the Conda environment for the project: 
    > conda env create --file environment.yml

- After packages have loaded, activate the new Conda environment:
    > conda activate feature_ranking

### Test the installation

- To run Python programs, change to the .\src folder: 
    > cd .\src

- The quick-demo program will dump a list of available OpenCL devices
  and run a very small OpenCL workload on each one: 
    > python quick_demo.py

- A few unit tests can be run:
    > python run_tests.py

### After a successful installation

- Run the main program: 
    > python feature_ranking.py

- More information on setup is available in the project [Wiki](https://github.com/cbmira01/FeatureRanking/wiki).

## More information

More information about feature ranking, OpenCL, the experimental approach of
this project, and results are described in the project [Wiki](https://github.com/cbmira01/FeatureRanking/wiki).

## Credits

Credits, attributions, and works consulted are summarized in the project [Wiki](https://github.com/cbmira01/FeatureRanking/wiki).

## Notes for Code Louisville project grading

This project fullfilled requirements for the Summer 2021 Code Louisville Python session.

- Implements a “master loop” console application where the user can repeatedly 
enter commands/perform actions, as seen in
    > ./src/feature_ranking.py

- Creates and uses a dictionary or list, as seen in  
    > ./src/prep_data.py

- Reads data from external JSON and CSV files, as seen in
    > ./src/prep_data.py

- Function calls that return values are used throughout, for example
    > ./src/fr_opencl.py
    > ./src/feature_ranking.py

- Implements a "stretch" goal: setup and testing of the OpenCL framework.
