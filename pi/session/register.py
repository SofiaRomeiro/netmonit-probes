import requests
import psutil as ps
from datetime import datetime
import netifaces as ni
from getmac import get_mac_address as getMacAddress
from constants import *
from monitor.configurations import Configurations
from env import PI_MODEL, PI_LOCATION, SERVER_PORT, SERVER_HOST

def setConfigurations(dg, timestamp):
   configs = Configurations()
   configs.destination_ip = dg
   configs.last_updated_monitor = timestamp
   configs.last_updated_external_performance = timestamp
   configs.last_updated_internal_performance = timestamp

def getIPAddress():
    ifaces = ps.net_if_addrs()
    tmp = ifaces.keys()
    print(tmp)
    if ETH_IFACE in tmp:
        return ifaces[ETH_IFACE][0][1], ETH_IFACE #IPv4
        #ifaces[ETH_IFACE][1][1].split('%')[0] #IPv6
    elif WLAN_IFACE in tmp:
        #ifaces[WLAN_IFACE][1][1].split('%')[0] #IPv6
        return ifaces[WLAN_IFACE][0][1], WLAN_IFACE #IPv4
    elif 'enp0s3' in tmp:
        #ifaces['enp1s0'][1][1].split('%')[0] #IPv6
        return ifaces['enp0s3'][0][1], 'enp0s3' #IPv4
    else:
        return None, None

def getGateway():
    gateways = ni.gateways()
    return gateways['default'][2][0]

def registration():

    ip, interface = getIPAddress()

    print("IP: " + str(ip))
    print("Interface: " + str(interface))

    if ip == None or interface == None:
        print("[LOG Register] Interface error")
        exit(1)

    mac = getMacAddress() # id is the mac address

    dg = getGateway()

    setConfigurations(dg, datetime.now())

    payload = {"id": mac,
                "location": PI_LOCATION, 
                "ip": ip, 
                "interface": interface,
                "model": PI_MODEL,
                "gateway": dg
                }
    
    print("Pi payload: " + str(payload))

    req = requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/registration", json=payload)

    print(req.status_code)

    return "Success on registration!!"