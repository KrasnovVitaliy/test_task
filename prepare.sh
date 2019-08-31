#!/usr/bin/env bash

export PYTHONPATH=$PYTHONPATH:$(pwd)
sudo pip3 install -r ./requirements.txt
python3 db/helpers.py
