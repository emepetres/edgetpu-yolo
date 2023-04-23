#!/bin/bash
set -e

sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y git curl gnupg

# Install PyCoral (you don't need to do this on a Coral Board)
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
sudo apt-get update
sudo apt-get install -y gasket-dkms libedgetpu1-std python3-pycoral

# Get Python dependencies
sudo apt-get install -y python3 python3-pip
pip3 install --upgrade pip setuptools wheel
python3 -m pip install numpy --user
python3 -m pip install opencv-python-headless --user
python3 -m pip install tqdm pyyaml --user

# Clone this repository
git clone git@github.com:emepetres/edgetpu-yolo.git
cd edgetpu-yolo
