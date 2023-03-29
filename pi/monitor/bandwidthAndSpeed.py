import sys
sys.path.append('..')
import speedtest
import psycopg2
from constants import *
from monitor.configurations import ProtocolOfPerformanceTest
from env import *
import iperf3
import json

def registExternalResult(download, upload, latency, destinationHost, timestamp, bytesSent, bytesReceived):
    try:
        connection = psycopg2.connect(LOCAL_DB_CONNECTION_STRING)
        cursor = connection.cursor()
        query = f"INSERT INTO externalPerformance (creation_date, upload_speed, \
            download_speed, latency, bytes_sent, bytes_received, destination_host) \
            VALUES (%s, %s, %s, %s, %s, %s, %s);"    
        data = (timestamp, upload, download, latency, bytesSent, bytesReceived, destinationHost)
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"[registResult(...)] An error occurred: {e}")
    finally:
        if connection is not None:
            connection.close()

def registInternalResult(creation_date, protocol, remote_host, jitter_ms, packet_loss, bytes_sent, bytes_received, sent_Mbps, received_Mbps):
    try:
        connection = psycopg2.connect(LOCAL_DB_CONNECTION_STRING)
        cursor = connection.cursor()
        query = f"INSERT INTO internalPerformance (creation_date, upload_speed, \
            download_speed, latency, bytes_sent, bytes_received, destination_host) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"    
        data = (creation_date, protocol, bytes_sent, bytes_received, jitter_ms, packet_loss, \
                sent_Mbps, received_Mbps, remote_host)
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"[registResult(...)] An error occurred: {e}")
    finally:
        if connection is not None:
            connection.close()

def iPerfTest(testType):
    client = iperf3.Client()
    client.server_hostname = IPERF_SERVER_HOST
    client.port = IPERF_SERVER_PORT
    client.json_output = True

    #################################################################
    #                                                               #
    # WARNING: iPerf3 has test type mistaken, so if you want udp,   #
    # you must ask for tcp, and vice-versa                          #
    #                                                               #
    #################################################################

    if (testType == ProtocolOfPerformanceTest.TCP):
        client.protocol = 'udp'
        return client.run()
    elif (testType == ProtocolOfPerformanceTest.UDP):
        client.protocol = 'tcp'
        return client.run()

def speedTest(server):
    servers=[]
    threads = None
    speed = speedtest.Speedtest()

    if server != None:
        servers.append(server)
        speed.get_servers(servers)
    else:
        speed.get_best_server()

    speed.download(threads=threads)
    speed.upload(threads=threads, pre_allocate=False)

    results = speed.results.dict()

    return results 

def parseUDP(res):
    print(f"[LOG] Result: {res}")
    try:
        creation_date = res['start']['timestamp']['time']
        remote_host = res['start']['connected'][0]['remote_host']
        sent_bytes = res['end']['sum_sent']['bytes'] 
        received_bytes = res['end']['sum_received']['bytes']
        #bits
        sent_Mbps = res['end']['sum_sent']['bits_per_second'] / 1000000000
        received_Mbps = res['end']['sum_received']['bits_per_second'] / 1000000000

        return registInternalResult(creation_date, 'UDP', remote_host, 'NULL', 'NULL', sent_bytes, received_bytes, sent_Mbps, received_Mbps)
    except Exception as e:
        print(f"[LOG Error] {str(e)}")

def parseTCP(res):
    print(f"[LOG] Result: {res}")
    try:
        creation_date = res['start']['timestamp']['time']
        remote_host = res['start']['connected'][0]['remote_host']

        jitter_ms = round(float(res['end']['sum']['jitter_ms']), 3)
        packet_loss = round(float(res['end']['sum']['lost_percent']), 3)
        bytes = res['end']['sum']['bytes'] 
        #bits
        Mbps = res['end']['sum']['bits_per_second'] / 1000000000

        return registInternalResult(creation_date, 'TCP', remote_host, jitter_ms, packet_loss, bytes, None, Mbps, None)    
    except Exception as e:
        print(f"[LOG Error] {str(e)}")

def testParserAndRegister(testType, res):
    if (testType == ProtocolOfPerformanceTest.TCP):
        parseTCP(res)
    else:
        parseUDP(res)

def measureExternalPerformance():

    speedTestResults = speedTest(None)
    download = speedTestResults['download']
    upload = speedTestResults['upload']
    latency = speedTestResults['ping']
    destinationHost = speedTestResults['server']['host']
    timestamp = speedTestResults['timestamp']
    bytesSent = speedTestResults['bytes_sent']
    bytesReceived = speedTestResults['bytes_received']

    registExternalResult(download, upload, latency, destinationHost, timestamp, bytesSent, bytesReceived)

def measureInternalPerformance():
    result = iPerfTest(ProtocolOfPerformanceTest.TCP)
    result_json = json.loads(str(result))
    testParserAndRegister(ProtocolOfPerformanceTest.TCP, result_json)
    