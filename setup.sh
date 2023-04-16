#!/bin/bash

sudo apt-get install -y iperf3
sudo docker-compose build
sudo docker-compose up