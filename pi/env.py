import os

#Database Variables
DB_USER = "pi"  
DB_PWD = "raspberry"
DB_HOST = "172.30.0.10" #docker container ip address - DON'T CHANGE
DB_NAME = "local_db"

#Remote Server Variables
SERVER_PORT = 8080
SERVER_HOST = "localhost"

#iPerf3 Server Variables
IPERF_SERVER_HOST = "0.0.0.0"
IPERF_SERVER_PORT = 2345

#RPi Variables
PI_MODEL = "Pi4"
PI_LOCATION = "Home"
PORT = int(os.getenv('PORT', "8082"))