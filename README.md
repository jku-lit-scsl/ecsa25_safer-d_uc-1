# SAFER-D: A Self-Adaptive Security Framework for Distributed Computing Architectures


This repository contains together with the webauthn sourcecode repository the supplemental material for SAFER-D.


This repository contains:

- Source code used for evaluating UC-1
- Instructions to run the project yourself (c.f. [Running the Project](#running-the-project))
- Evaluation (c.f. [Evaluation](#evaluation))
  - Jupyter Notebooks used for the evaluation of UC-1
  - Jupyter Notebook used for the evaluation of UC-2 (Webauthn)
  - Raw Log-Data and Timing measurements of UC-1 and UC-2
- Additional files for the local MAPE-K loop integration (c.f. [Additional](#additional)))

# Use Case 1: Edge Computing for machine manufacturing

![hierachy_img](https://github.com/jku-lit-scsl/seams25-sec-arch/blob/master/uc-1-arch-v2.png)

Note: The numbers in the image were simplified in the paper. 
For better traceability, the numbers here correspond to the last digits of the respective IP addresses in the evaluation.

## Running the Project

### Setup

Install required packages ([resources.txt](config/resources.txt))

```
pip install -r config/resources.txt
```

Run `main.py` with sudo

### Windows Additional Setup

For ICMP sniffing "npcap" will be necessary: https://npcap.com/#download

### Additioanal Packages required to rerun the Jupyter Notebooks

Additional Python Packages Required

```
pandas
matplotlib
seaborn 
scikit-learn
```

### Other useful commands

```bash

# Set up Git credential caching
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=43200'

# Create a Python virtual environment
python3.11 -m venv venv311
source venv311/bin/activate

# Install requirements from requirements
pip install -r resources/requirements.txt

# Display the path of the Python interpreter
which python

# Deactivate the virtual environment
deactivate

# to execute the program vai the virtual environment
sudo venv311/bin/python main.py

# git commands for switching branch
git remote add origin https://github.com/jku-lit-scsl/seams25-sec-arch.git
git fetch origin

# see whats running on port 5000
sudo lsof -i :5000

# kill the process with the ID 1234
sudo kill 1234
```

# Evaluation

## Jupyter Notebooks used for the evaluation of UC-1

Files:

[00_uc-1_sec_lvl_eval.ipynb](eval/00_uc-1_sec_lvl_eval.ipynb)

[01_uc-1_meta-adapt_eval.ipynb](eval/01_uc-1_meta-adapt_eval.ipynb)

## Jupyter Notebook used for the evaluation of UC-2

File:

[02_uc-2_sec_lvl_eval.ipynb](eval/02_uc-2_sec_lvl_eval.ipynb)

## Raw Log-Data and Timing measurements of UC-1 and UC-2

Files:

[raw](eval/raw)

# Additional

Find an example local default mape-k control file in
[default_mape_example.txt](additional_files/default_mape_example.txt)
