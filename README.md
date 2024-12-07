## Setup

required packages


```
pip install flask requests python-statemachine psutil pytz
```

Note: `pip3` on mac

### Windows Additional Setup

For ICMP sniffing "npcap" will be necessary: https://npcap.com/#download

## Other useful commands

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
```