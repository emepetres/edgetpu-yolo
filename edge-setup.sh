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
python3 -m pip install numpy==1.24.* --user
python3 -m pip install opencv-python-headless==4.7.* --user
python3 -m pip install tqdm4.65.* pyyaml==6.0 flask==2.2.* --user

# Clone this repository
git clone https://github.com/emepetres/edgetpu-yolo.git
cd edgetpu-yolo
