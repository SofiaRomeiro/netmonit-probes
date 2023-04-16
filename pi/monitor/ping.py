import netifaces
from datetime import datetime
import psycopg2
import pingparsing
import statistics
from constants import *
from monitor.configurations import Configurations

ping_parser = pingparsing.PingParsing()
transmitter = pingparsing.PingTransmitter()

def resultParser(number):
    return 0 if number == None else number

def getDestinationIP():
    configs = Configurations()
    print(f"[LOG Ping]Destination IP: {configs.destination_ip}", flush=True)
    return configs.destination_ip

def ping(ping_count, ping_destination, ping_interface): 
    transmitter.interface = ping_interface
    transmitter.destination = ping_destination   
    transmitter.count = ping_count
    return transmitter.ping()

def measureJitter(ping_destination, ping_interface):
    t = pingparsing.PingTransmitter()
    t.interface = ping_interface
    t.destination = ping_destination   
    t.count = 10
    tmp = (t.ping())[0].split(' ')
    result = list(filter(lambda x: ("time" in x), tmp))
    latencies = list(map(lambda x: (x[5:9]), result))[0: len(result)-1]
    return statistics.variance([float(x, 3) for x in latencies])

def registerPingResult(destination_ip, max, min, avg, packets_sent, packets_received, packet_loss, jitter, interface):
    try:
        connection = psycopg2.connect(LOCAL_DB_CONNECTION_STRING)
        cursor = connection.cursor()
        query = f"INSERT INTO events (creation_date, destination_ip, max, min, avg, packets_sent, packets_received, packet_loss, jitter, interface) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"    
        data = (datetime.now(), destination_ip, max, min, avg, packets_sent, packets_received, packet_loss, jitter, interface)
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"[registerPingResult(...)] An error occurred: {e}", flush=True)
    finally:
        if connection is not None:
            connection.close()

def pingFromInterface(interface, number_of_pings):

    ping_destination = getDestinationIP()
    ping(1,ping_destination, interface) #result isn't relevant

    result = ping(number_of_pings, ping_destination, interface)
    result_dict = ping_parser.parse(result).as_dict()

    print("[LOG Monitor Ping] Ping result: " + str(result_dict), flush=True)

    rtt_max = resultParser(result_dict[MAX_PING])
    rtt_min = resultParser(result_dict[MIN_PING])
    rtt_avg = resultParser(result_dict[AVG_PING])
    packets_sent = result_dict[SENT]
    packets_received = result_dict[RECEIVED]
    packet_loss = result_dict[PACKET_LOSS]

    jitter = measureJitter(ping_destination, interface)

    registerPingResult(ping_destination, rtt_max, rtt_min, rtt_avg, packets_sent, packets_received, packet_loss, jitter, interface)

    return packet_loss

def monitorPing():
    try:
        gateways = netifaces.gateways()  
        print("Gateways: " + str(gateways), flush=True)  
        interface = gateways['default'][netifaces.AF_INET][1]

        packet_loss = pingFromInterface(interface, 5)

        active_interfaces_count = len(gateways[2])

        if packet_loss == 100 and active_interfaces_count == 2: # try pinging with the wireless interface
            
            interface = gateways[2][1][1]        
            pingFromInterface(interface, 5)


    except Exception as e: # when the device is not connected to a network and have no IP, an exception will be throw
        print(f"[monitorPing()] An error occurred: {e}", flush=True)
        registerPingResult(getDestinationIP(), 0, 0, 0, 0, 0, 0, gateways['default'][netifaces.AF_INET][1])
