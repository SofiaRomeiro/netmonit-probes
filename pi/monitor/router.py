import requests
import json
from datetime import datetime
from fastapi import APIRouter
from monitor.configurations import Configurations, TypeOfUpdate
from monitor.ping import monitorPing
from monitor.update import retrieveDataFromEvents as updateMonitor
from monitor.update import retrieveDataFromPerformance as updatePerformance
from monitor.check_ip import monitorUpdateIp as updateIp
from monitor.bandwidthAndSpeed import measurePerformance
from monitor.change_dest_ping import monitorChangeDestPing as changeDestPing
from env import SERVER_PORT, SERVER_HOST
from constants import SUCCESS

router = APIRouter()

configs = Configurations()

def updateConfigurations(type):
    if (type == TypeOfUpdate.MONITOR):
        configs.last_updated_monitor = datetime.now()
    elif (type == TypeOfUpdate.PERFORMANCE):
        configs.last_updated_performance = datetime.now()

@router.get("/ping")
def pingController():
    return monitorPing()

@router.get("/update/ping")
def updateMonitorController():

    #define if is a local update or a remote update
    id, result = updateMonitor()
    print("[LOG Router - Update Ping] Result: " + str(result))
    payload_list = []
    for res in result:
        time = str(res[0])
        max = str(res[2])
        min = str(res[3])
        avg = str(res[4])
        packets_sent = str(res[5])
        packets_received = str(res[6]) 
        packet_loss = str(res[7])
        jitter = str(res[8])
        tmp = {
            "id_pi": id,
            "creation_date": time,
            "destination_ip": res[1],
            "max": max,
            "min": min,
            "avg": avg,
            "packets_sent": packets_sent,
            "packets_received": packets_received, 
            "packet_loss": packet_loss, 
            "jitter": jitter,
            "interface": res[9]
        }
        payload_list.append(tmp)
    
    payload = json.dumps(payload_list, indent=4)

    print("[LOG] Payload: " + payload)

    response = requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/update/monitor", json=json.loads(payload))
    if (response.status_code == SUCCESS):
        updateConfigurations(TypeOfUpdate.MONITOR)
        return response.status_code
    else:
        return f"{str(response.status_code)}: {str(response.status)}"

@router.get("/check-ip")
def checkIpController():
    return updateIp()

@router.get("/performance")
def speedTestController():
    return measurePerformance()

@router.get("/update/performance")
def updatePerformanceController():
    id, result = updatePerformance()
    payload_list = []
    print("Res:" + str(result))
    for res in result:
        creation_date = str(res[0])
        upload_speed = str(res[1])
        download_speed = str(res[2])
        latency = str(res[3])
        bytes_sent = str(res[4])
        bytes_received = str(res[5])
        destination_host = str(res[6])
        tmp = {
            "id_pi": id,
            "creation_date": creation_date,
            "upload_speed": upload_speed,
            "download_speed": download_speed,
            "latency": latency,
            "bytes_sent": bytes_sent,
            "bytes_received": bytes_received,
            "destination_host": destination_host
        }
        payload_list.append(tmp)
    
    payload = json.dumps(payload_list, indent=4)

    print("[LOG] Payload: " + payload)

    response = requests.post(f"http://{SERVER_HOST}:{SERVER_PORT}/api/probes/update/performance", json=json.loads(payload))
    if (response.status_code == SUCCESS):
        updateConfigurations(TypeOfUpdate.PERFORMANCE)
        return response.status_code
    else:
        return f"{str(response.status_code)}: {str(response.status)}"

# receives request from main-server
@router.put("/change-dest-ip/{ip_address}")
def changeDestPingController(ip_address: str):
    return changeDestPing(ip_address, configs)
