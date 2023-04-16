#!/bin/bash

#setup pi variables
echo "Starting bash script..."

name="NAME = '"$1"'"
location="PI_LOCATION = '"$2"'"
model="PI_MODEL = '"$3"'"

echo "" >> "./pi/env.py"
echo "$name" >> "./pi/env.py"
echo "$location" >> "./pi/env.py"
echo "$model" >> "./pi/env.py"

sleep 1

sudo apt-get install -y iperf3
sudo docker-compose build
sudo docker-compose up
