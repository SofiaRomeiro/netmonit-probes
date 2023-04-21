import sys
sys.path.append('..')
import speedtest
import psycopg2
from datetime import datetime
from constants import *
from env import *

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
        print(f"\x1b[6;30;41m [ERROR - Regist External Result] An error occurred: {e} \x1b[0m", flush=True)
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

    return speed.results.dict()

def measureExternalPerformance():

    print("\x1b[6;30;45m[LOG] Running External Performance Measurement", flush=True + "\x1b[0m")

    speedTestResults = speedTest(None)
    # (replacing) speedtest original timestamp is UTC, which shows wrong results in Portugal
    timestamp = datetime.now()

    print(f"[LOG External Performance @ {timestamp}] Results: {str(speedTestResults)}", flush=True)

    registExternalResult(
        speedTestResults['download']/1000000, #Mbps
        speedTestResults['upload']/1000000, #Mbps
        speedTestResults['ping'], #measures latency 
        speedTestResults['server']['host'], 
        timestamp, 
        speedTestResults['bytes_sent'], 
        speedTestResults['bytes_received']
    )

