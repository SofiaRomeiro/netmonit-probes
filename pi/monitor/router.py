import requests
import json
from fastapi import APIRouter
from monitor.configurations import Configurations, TypeOfUpdate, TypeOfPerformanceTest
from monitor.ping import monitorPing
from monitor.check_ip import monitorUpdateIp as updateIp
from monitor.bandwidthAndSpeed import measureInternalPerformance, measureExternalPerformance
from pi.monitor.changeDestPing import monitorChangeDestPing as changeDestPing
from env import SERVER_PORT, SERVER_HOST
from constants import SUCCESS
from pi.monitor.auxiliaryFunctions import *

router = APIRouter()

configs = Configurations()

@router.get("/ping")
def pingController():
    return monitorPing()

@router.get("/update/ping")
def updateMonitorController():

    payload = updatePingOperation()
    print("[LOG - Router] Update GET Payload: " + payload)
    response = requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/update/monitor", json=json.loads(payload))
    if (response.status_code == SUCCESS):
        updateConfigurations(TypeOfUpdate.MONITOR)
        return response.status_code
    else:
        return f"{str(response.status_code)}: {str(response.status)}"

@router.get("/check-ip")
def checkIpController():
    return updateIp()

@router.get("/performance/internal")
def performanceController():
    return measureInternalPerformance()

@router.get("/performance/external")
def performanceController():
    return measureExternalPerformance()

@router.get("/update/performance/internal")
def updateInternalPerformanceController():   
    
    payload = updatePerformanceOperation(TypeOfPerformanceTest.INTERNAL)

    print("[LOG - Router] Performance GET Payload: " + payload)

    response = requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/update/performance/internal", json=json.loads(payload))
    if (response.status_code == SUCCESS):
        updateConfigurations(TypeOfUpdate.EXTERNAL_PERFORMANCE)
        return response.status_code
    else:
        return f"{str(response.status_code)}: {str(response.text)}"
    
@router.get("/update/performance/external")
def updateExternalPerformanceController():   
    
    payload = updatePerformanceOperation(TypeOfPerformanceTest.EXTERNAL)

    print("[LOG - Router] Performance GET Payload: " + payload)

    response = requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/update/performance/external", json=json.loads(payload))
    if (response.status_code == SUCCESS):
        updateConfigurations(TypeOfUpdate.EXTERNAL_PERFORMANCE)
        return response.status_code
    else:
        return f"{str(response.status_code)}: {str(response.text)}"

# Requests from Server

@router.put("/change-dest-ip/{ip_address}")
def changeDestPingController(ip_address: str):
    return changeDestPing(ip_address, configs)

@router.post("/update/ping")
async def changeDestPingController():
    payload = updatePingOperation()
    print("[LOG - Router] Update POST Payload: " + payload)

    try:
        response = await requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/update/monitor", json=json.loads(payload))
        if (response.status_code == SUCCESS):
            updateConfigurations(TypeOfUpdate.MONITOR)
            return response.status_code
        else:
            return f"{str(response.status_code)}: {str(response.status)}"
    except Exception as e:
        print(f"[LOG] Error: {str(e.with_traceback)}")

@router.post("/update/performance/external")
async def updatePerformanceController():   
    
    payload = updatePerformanceOperation(TypeOfPerformanceTest.INTERNAL)

    print("[LOG - Router] Performance GET Payload: " + payload)

    try:
        response = await requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/update/performance", json=json.loads(payload))
        if (response.status_code == SUCCESS):
            updateConfigurations(TypeOfUpdate.EXTERNAL_PERFORMANCE)
            return response.status_code
        else:
            return f"{str(response.status_code)}: {str(response.text)}"
    except Exception as e:
        print(f"[LOG] Error: {str(e.with_traceback)}")
    
@router.post("/update/performance/internal")
def updatePerformanceController():   
    
    payload = updatePerformanceOperation(TypeOfPerformanceTest.INTERNAL)

    print("[LOG - Router] Performance GET Payload: " + json.loads(payload))

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    try:
        response = requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/update/performance", data=json.dumps(json.loads(payload)), headers=headers)
        print(f"Response: {str(response.status_code)}: {str(response.text)}")
        if (response.status_code == SUCCESS):
            updateConfigurations(TypeOfUpdate.EXTERNAL_PERFORMANCE)
            print(f"Response: {str(response.status_code)}: {str(response.text)}")
        else:
            print(f"Response: {str(response.status_code)}: {str(response.text)}")  
    except Exception as e:
        print(f"[LOG] Error: {str(e.with_traceback)}")
    