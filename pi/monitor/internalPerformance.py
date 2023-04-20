import sys
sys.path.append('..')
import psycopg2
from datetime import datetime
import json
from constants import *
from monitor.configurations import ProtocolOfPerformanceTest
from env import *
import subprocess as sp

def registInternalResult(creation_date, protocol, remote_host, jitter_ms, packet_loss, bytes_sent, bytes_received, sent_Mbps, received_Mbps):
    try:
        #filter by protocol
        query = ""
        data = None
        if (protocol == ProtocolOfPerformanceTest.UDP):
            query = f"INSERT INTO internalPerformance (creation_date, protocol, \
            bytes_sent, jitter, packet_loss, sent_Mbps, destination_host) \
            VALUES (%s, %s, %s, %s, %s, %s, %s);"  
            data = (creation_date, "UDP", bytes_sent, jitter_ms, packet_loss, \
                sent_Mbps, remote_host)
        else:        
            query = f"INSERT INTO internalPerformance (creation_date, protocol, \
            bytes_sent, bytes_received, sent_Mbps, received_Mbps, destination_host) \
            VALUES (%s, %s, %s, %s, %s, %s, %s);"    
            data = (creation_date, "TCP", bytes_sent, bytes_received, \
                    sent_Mbps, received_Mbps, remote_host)            
        connection = psycopg2.connect(LOCAL_DB_CONNECTION_STRING)
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"[LOG registInternalResult(...)] An error occurred: {e}", flush=True)
    finally:
        if connection is not None:
            connection.close()

'''def iPerfTest(testType):

    try:
        client = iperf3.Client()
        client.server_hostname = IPERF_SERVER_HOST
        client.port = IPERF_SERVER_PORT
        client.json_output = True
        if (testType == ProtocolOfPerformanceTest.TCP):
            client.protocol = 'tcp'
            return client.run()
        elif (testType == ProtocolOfPerformanceTest.UDP):
            client.protocol = 'udp'
            return client.run()
    except Exception as e:
        print(f"[LOG iPerf] ERROR: {str(e)}", flush=True)'''

def parseUDP(res):
    try:
        creation_date = datetime.now()
        print(f"[LOG parseUDP {creation_date}] Result: {res}", flush=True)
        return registInternalResult(
                creation_date, 
                ProtocolOfPerformanceTest.UDP, 
                res['start']['connected'][0]['remote_host'], 
                res['end']['sum']['jitter_ms'], 
                res['end']['sum']['lost_packets'], 
                res['end']['sum']['bytes'], 
                'NULL', 
                res['end']['sum']['bits_per_second'] / 1000000000, 
                'NULL'
            )    
    except Exception as e:
        print(f"[LOG Error] {str(e)}", flush=True)

def parseTCP(res):
    try:
        creation_date = datetime.now()
        print(f"[LOG parseTCP {creation_date}] Result: {res}")
        return registInternalResult(
                creation_date, 
                ProtocolOfPerformanceTest.TCP, 
                res['start']['connected'][0]['remote_host'], 
                'NULL', 
                'NULL', 
                res['end']['sum_sent']['bytes'] * 8, 
                res['end']['sum_received']['bytes'], 
                res['end']['sum_sent']['bits_per_second'] / 1000000000, 
                res['end']['sum_received']['bits_per_second'] / 1000000000
            )

    except Exception as e:
        print(f"[LOG Error] {str(e)}", flush=True)

def testParserAndRegister(testType, res):
    if (testType == ProtocolOfPerformanceTest.TCP):
        parseTCP(res)
    else:
        parseUDP(res)

def iPerf3Test(testType):
    command = f"sudo iperf3 -c {IPERF_SERVER_HOST} -p {IPERF_SERVER_PORT} -t 30s -i 1 -O 1 -J"
    if testType == ProtocolOfPerformanceTest.UDP:
        command += " -u"
    result = sp.getoutput(command)
    return json.loads(result)

def measureInternalPerformance():
    print("\x1b[6;30;42m" + "[LOG Internal Performance] Start Measurement" + "\x1b[0m", flush=True)
    try:
        testParserAndRegister(
            ProtocolOfPerformanceTest.TCP, 
            iPerf3Test(ProtocolOfPerformanceTest.TCP)
        )
    except Exception as e:
        print("[LOG Error] Internal Performance: " + str(e, encoding='utf-8'), flush=True)

'''def measureInternalPerformance():
    try:
        result = iPerfTest(ProtocolOfPerformanceTest.TCP)
        try:
            result_json = json.loads(str(result))
        except Exception as e:
            print("[LOG - Internal Performance] Parsing error: " + str(e))
        testParserAndRegister(ProtocolOfPerformanceTest.TCP, result_json)
    except Exception as e:
        print("[LOG Error] Internal Performance: " + str(e, encoding='utf-8'))'''
