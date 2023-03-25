import requests
import psycopg2
from datetime import datetime
import netifaces as ni
from getmac import get_mac_address as getMacAddress
from monitor.configurations import Configurations
from constants import ETH0_INTERFACE, LOCAL_DB_CONNECTION_STRING
from env import PI_MODEL, PI_LOCATION, SERVER_PORT, SERVER_HOST

def setConfigurations(dg, timestamp):
   configs = Configurations()
   configs.destination_ip = dg
   configs.last_updated = timestamp

def getIPAddress():
    ip = ni.ifaddresses(ETH0_INTERFACE)[ni.AF_INET][0]['addr']
    return ip

def getGateway():
    gateways = ni.gateways()
    return gateways['default'][2][0]

def registration():

    ip = getIPAddress()

    mac = getMacAddress() # id is the mac address

    dg = getGateway()

    setConfigurations(dg, datetime.now())

    payload = {"id": mac,
                "location": PI_LOCATION, 
                "ip": ip, 
                "model": PI_MODEL,
                "gateway": dg
                }
    
    print("Pi payload: " + str(payload))

    req = requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/registration", json=payload)

    print(req.status_code)

    return "Success on registration!!"