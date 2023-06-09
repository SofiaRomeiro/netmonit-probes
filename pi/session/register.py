import requests
import psutil as ps
from datetime import datetime
import netifaces as ni
from getmac import get_mac_address as getMacAddress
from constants import *
from monitor.configurations import Configurations
from env import PI_MODEL, PI_LOCATION, NAME, SERVER_PORT, SERVER_HOST

def setConfigurations(dg, timestamp):
   configs = Configurations()
   configs.destination_ip = dg
   configs.last_updated_monitor = timestamp
   configs.last_updated_external_performance = timestamp
   configs.last_updated_internal_performance = timestamp
   configs.last_updated_wifi_test = timestamp

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
    elif VM_IFACE in tmp:
        #ifaces[VM_IFACE][1][1].split('%')[0] #IPv6
        return ifaces[VM_IFACE][0][1], VM_IFACE #IPv4
    else:
        return None, None

def getGateway():
    gateways = ni.gateways()
    return gateways['default'][2][0]

def registration():

    try:
        ip, interface = getIPAddress()

        if ip == None or interface == None:
            print(f"\x1b[6;30;41m [ERROR - Registration] Probe Not Connected \x1b[0m", flush=True)
            exit(1)

        mac = getMacAddress() # id is the mac address
        dg = getGateway()
        setConfigurations(dg, datetime.now())

        payload = {"id": mac,
                    "name": NAME,
                    "location": PI_LOCATION, 
                    "ip": ip, 
                    "interface": interface,
                    "model": PI_MODEL,
                    "gateway": dg
                    }    
        headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/51.0.2704.103 \
                Safari/537.36"}
        
        print(f"\x1b[6;30;46m [LOG - Registration] Probe's Payload: {str(payload)} \x1b[0m", flush=True)

        requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/registration", json=payload, headers=headers)

        print(f"\x1b[6;30;42m [LOG - Registration] Probe Successfully Registered \x1b[0m", flush=True)
        return SUCCESS_MESSAGE
    
    except Exception as e:
        print(f"\x1b[6;30;41m [ERROR - Registration] An error ocurred: {str(e)} \x1b[0m", flush=True)
