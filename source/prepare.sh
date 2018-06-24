#!/usr/bin/env bash

echo "Preparing environment for Grazer system"

echo "Installing Python 3"
sudo apt-get install python3.5

echo "Installing ffmpeg"
sudo apt-get install ffmpeg

echo "Creating virtual env for Grazer source"
sudo python3 -m pip install virtualenv
python3 -m virtualenv venv
echo "Activating virtualenv (venv)"
source ./venv/bin/activate

echo "Install required python module in virtualenv"
pip install -r requirements.txt
