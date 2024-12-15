# SHIELD: A Self-Adaptive Security Framework for Hierarchical Software Systems

This repository contains:
- Source code used for evaluating UC-1
- Instructions to run the project yourself (c.f. [Running the Project](#running-the-project)
- Evaluation (c.f. [Evaluation](#evaluation))
  - Jupyter Notebooks used for the evaluation of UC-1
  - Jupyter Notebook used for the evaluation of UC-2
  - Raw Log-Data and Timing measurements of UC-1 and UC-2

# Use Case 1: Edge Computing

![hierachy_img](https://github.com/jku-lit-scsl/seams25-sec-arch/blob/master/uc-1-arch-v2.png)


## Running the Project 

### Setup

Install required packages ([resources.txt](config%2Fresources.txt))

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





