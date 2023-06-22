import time
import requests
import json
from fastapi import APIRouter
from monitor.configurations import Configurations, TypeOfUpdate, TypeOfPerformanceTest
from monitor.ping import monitorPing
from monitor.internalPerformance import measureInternalPerformance
from monitor.externalPerformance import measureExternalPerformance
from monitor.changeDestPing import monitorChangeDestPing as changeDestPing
from monitor.auxiliaryFunctions import *
from env import SERVER_PORT, SERVER_HOST
from constants import SUCCESS

router = APIRouter()

configs = Configurations()

def updateMonitor():
    payload = updatePingOperation()
    response = requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/update/monitor", json=json.loads(payload))
    if (response.status_code == SUCCESS):
        updateConfigurations(TypeOfUpdate.MONITOR)
        print(f"\x1b[6;30;42m [LOG Router - updateMonitor] Ping Results Successfully Registered on Server\x1b[0m", flush=True)
        return response.status_code
    else:
        print(f"\x1b[6;30;43m [LOG Router - updateMonitor] Update Configurations Unsuccessful\x1b[0m", flush=True)
        return f"{str(response.status_code)}: {str(response.status)}"

def updateInternalPerformance():
    payload = updatePerformanceOperation(TypeOfPerformanceTest.INTERNAL)
    response = requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/update/performance/internal", json=json.loads(payload))
    if (response.status_code == SUCCESS):
        updateConfigurations(TypeOfUpdate.INTERNAL_PERFORMANCE)
        print(f"\x1b[6;30;42m [LOG Router - updateInternalPerformance] Performance Results Successfully Registered on Server\x1b[0m", flush=True)
        return response.status_code
    else:
        print(f"\x1b[6;30;43m [LOG Router - updateInternalPerformance] Update Configurations Unsuccessful\x1b[0m", flush=True)
        return f"{str(response.status_code)}: {str(response.text)}"

def updateExternalPerformance():
    payload = updatePerformanceOperation(TypeOfPerformanceTest.EXTERNAL)
    response = requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/update/performance/external", json=json.loads(payload))
    if (response.status_code == SUCCESS):
        updateConfigurations(TypeOfUpdate.EXTERNAL_PERFORMANCE)
        print(f"\x1b[6;30;42m [LOG Router - updateInternalPerformance] Performance Results Successfully Registered on Server\x1b[0m", flush=True)
        return response.status_code
    else:
        print(f"\x1b[6;30;43m [LOG Router - updateExternalPerformance] Update Configurations Unsuccessful\x1b[0m", flush=True)
        return f"{str(response.status_code)}: {str(response.text)}"

def updateWifiTest():
    payload = updateWifiTestOperation()
    response = requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/update/wifitest", json=json.loads(payload))
    if (response.status_code == SUCCESS):
        updateConfigurations(TypeOfUpdate.WIFI)
        print(f"\x1b[6;30;42m [LOG Router - updateMonitor] WiFi Results Successfully Registered on Server\x1b[0m", flush=True)
        return response.status_code
    else:
        print(f"\x1b[6;30;43m [LOG Router - updateMonitor] Update Configurations Unsuccessful\x1b[0m", flush=True)
        return f"{str(response.status_code)}: {str(response.status)}"


#####################################################
#                                                   #
#                    GET Requests                   #
#                                                   #
#####################################################

@router.get("/ping")
def pingController():
    return monitorPing()

@router.get("/update/ping")
def updateMonitorController():
    return updateMonitor()    

@router.get("/performance/internal")
def internalPerformanceController():
    return measureInternalPerformance()

@router.get("/update/performance/internal")
def updateInternalPerformanceController():   
    return updateInternalPerformance()    

@router.get("/performance/external")
def externalPerformanceController():
    return measureExternalPerformance()
    
@router.get("/update/performance/external")
def updateExternalPerformanceController():   
    return updateExternalPerformance()   

#####################################################
#                                                   #
#                PUT/POST Requests                  #
#                                                   #
#####################################################

@router.put("/change-dest-ip/{ip_address}")
def changeDestPingController(ip_address: str):
    return changeDestPing(ip_address, configs)

@router.post("/update/ping")
def changeDestPingController():
    return updateMonitor()
    
@router.post("/update/performance/internal")
def updateInternalPerformanceController():       
    return updateInternalPerformance() 

@router.post("/update/performance/external")
def updateExternalPerformanceController():       
    return updateExternalPerformance() 
    
