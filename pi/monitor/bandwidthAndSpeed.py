import sys
sys.path.append('..')
import speedtest
import psycopg2
from constants import *
import iperf3

def registResult(download, upload, latency, destinationHost, timestamp, bytesSent, bytesReceived):
    try:
        connection = psycopg2.connect(LOCAL_DB_CONNECTION_STRING)
        cursor = connection.cursor()
        query = f"INSERT INTO performance (creation_date, upload_speed, \
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

def measurePerformance():

    speedTestResults = speedTest(None)
    download = speedTestResults['download']
    upload = speedTestResults['upload']
    latency = speedTestResults['ping']
    destinationHost = speedTestResults['server']['host']
    timestamp = speedTestResults['timestamp']
    bytesSent = speedTestResults['bytes_sent']
    bytesReceived = speedTestResults['bytes_received']

    client = iperf3.Client()
    client.server_hostname="192.168.137.208"
    client.port = 2345
    client.json_output = True
    result = client.run()

    registResult(download, upload, latency, destinationHost, timestamp, bytesSent, bytesReceived)
    