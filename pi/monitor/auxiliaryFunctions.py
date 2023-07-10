import json
from datetime import datetime
from monitor.configurations import TypeOfUpdate, Configurations, TypeOfPerformanceTest
from monitor.update import retrieveDataFromEvents as updateMonitor
from monitor.update import retrieveDataFromExternalPerformance as updateExternalPerformance
from monitor.update import retrieveDataFromInternalPerformance as updateInternalPerformance
from monitor.update import retrieveDataFromWifiTest as updateWifiTest

def updatePingOperation():
    try:
        id, result = updateMonitor()
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
        
        return payload
    except Exception as e:
        print(f"\x1b[6;30;41m [LOG updatePingOperation] An error ocurred: {str(e)}\x1b[0m", flush=True)
        

def updateInternal():
    id, result = updateInternalPerformance()
    payload_list = []
    for res in result:
        creation_date = str(res[0]) 
        protocol = str(res[1])
        bytes_sent = str(res[2])
        bytes_received = str(res[3])
        jitter = str(res[4])
        packet_loss = str(res[5])
        sent_Mbps = str(res[6])
        received_Mbps = str(res[7])
        destination_host = str(res[8])
        tmp = {
            "id_pi": id,
            "creation_date": creation_date,
            "protocol": protocol,
            "bytes_sent": bytes_sent,
            "bytes_received": bytes_received,
            "jitter": jitter,
            "packet_loss": packet_loss,
            "sent_Mbps": sent_Mbps,
            "received_Mbps": received_Mbps,
            "destination_host": destination_host
        }
        payload_list.append(tmp)
    
    payload = json.dumps(payload_list, indent=4)
    return payload

def updateExternal():
    id, result = updateExternalPerformance()
    payload_list = []
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
    return payload

def updatePerformanceOperation(type):
    try:
        if (type == TypeOfPerformanceTest.INTERNAL):
            return updateInternal()
        else:
            return updateExternal()        
    except Exception as e:
        print(f"\x1b[6;30;41m [LOG updatePerformanceOperation] An error ocurred: {str(e)}\x1b[0m", flush=True)

def updateWifiTestOperation():
    id, result = updateWifiTest()
    payload_list = []
    for res in result:
        creation_date = str(res[0]) 
        ap = str(res[1])
        channel = str(res[2])
        frequency = str(res[3])
        quality = str(res[4])
        signal_level = str(res[5])
        encryption_mode = str(res[6])
        essid = str(res[7])
        tmp = {
            "id_pi": id,
            "creation_date": creation_date,
            "ap": ap,
            "channel": channel,
            "frequency": frequency,
            "quality": quality,
            "signal_level": signal_level,
            "encryption_mode": encryption_mode,
            "essid": essid
        }
        payload_list.append(tmp)
    
    payload = json.dumps(payload_list, indent=4)
    return payload

def updateConfigurations(type):
    configs = Configurations()
    if (type == TypeOfUpdate.MONITOR):
        configs.last_updated_monitor = datetime.now()
    elif (type == TypeOfUpdate.EXTERNAL_PERFORMANCE):
        configs.last_updated_external_performance = datetime.now()
    elif (type == TypeOfUpdate.INTERNAL_PERFORMANCE):
        configs.last_updated_internal_performance = datetime.now()
    elif (type == TypeOfUpdate.WIFI):
        configs.last_updated_wifi_test = datetime.now()
