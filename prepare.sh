#!/usr/bin/env bash

export PYTHONPATH=$PYTHONPATH:/home/vitaliy/test_task
sudo pip3 install -r ./requirements.txt
python3 db/helpers.py