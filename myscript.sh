#!/bin/bash

# Update the package manager and install necessary development tools
sudo dnf update -y
sudo dnf groupinstall "Development Tools" -y

# Install Python 3 and pip
sudo dnf install python3 python3-pip -y

# Create a Python 3 virtual environment
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages and dependencies
    pip install pyparsing
    pip install appdirs
    pip install setuptools==40.1.0
    pip install cryptography==2.8
    pip install bcrypt==3.1.7
    pip install PyNaCl==1.3.0
    pip install Fabric3==1.14.post1

# Deactivate the virtual environment when you're done
deactivate