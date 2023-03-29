# Network Monitoring - Probes Software
This repository includes the code that is specific to run on the probes

## Setup

1. Clone the repository
2. Install `docker` and `docker-compose`
3. In case you have postgres installed, stop the service by typing `sudo systemctl stop postgresql` in cmd
4. Edit the configuration files
5. Go to the directory that contains the `Dockerfile` and `docker-compose.yml`. 
6. Once the image is built, run `sudo docker-compose up`. 
    - Note that this might take a while due to the image setup.
