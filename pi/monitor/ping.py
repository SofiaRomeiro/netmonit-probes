import netifaces
from datetime import datetime
from tcp_latency import measure_latency
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
    print(f"\x1b[6;30;46m [LOG Ping] Destination IP: {configs.destination_ip}\x1b[0m", flush=True)
    return configs.destination_ip

def ping(ping_count, ping_destination, ping_interface): 
    transmitter.interface = ping_interface
    transmitter.destination = ping_destination   
    transmitter.count = ping_count
    return transmitter.ping()

def measureJitter(ping_destination):
    try:
        return statistics.variance(measure_latency(ping_destination, runs=10))
    except Exception as e:
        print(f"\x1b[6;30;41m [LOG Ping - Measure Jitter] An error ocurred: {str(e)}\x1b[0m", flush=True)
        return NO_RESULT

def registerPingResult(destination_ip, max, min, avg, packets_sent, packets_received, packet_loss, jitter, interface):
    try:
        connection = psycopg2.connect(LOCAL_DB_CONNECTION_STRING)
        cursor = connection.cursor()
        query = ""
        data = None
        if jitter == NO_RESULT:
            query = f"INSERT INTO events (creation_date, destination_ip, max, min, avg, packets_sent, packets_received, packet_loss, interface) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            data = (datetime.now(), 
                    destination_ip, 
                    max, 
                    min, 
                    avg, 
                    packets_sent, 
                    packets_received, 
                    packet_loss, 
                    interface
                )
        else:
            query = f"INSERT INTO events (creation_date, destination_ip, max, min, avg, packets_sent, packets_received, packet_loss, jitter, interface) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"    
            data = (datetime.now(), 
                        destination_ip, 
                        max, 
                        min, 
                        avg, 
                        packets_sent, 
                        packets_received, 
                        packet_loss, 
                        jitter, 
                        interface
                    )            
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"\x1b[6;30;41m [LOG Ping - DB] An error ocurred: {str(e)}\x1b[0m", flush=True)
    finally:
        if connection is not None:
            connection.close()

def pingFromInterface(interface, number_of_pings):

    ping_destination = getDestinationIP()
    ping(1,ping_destination, interface) #result isn't relevant

    result = ping(number_of_pings, ping_destination, interface)
    result_dict = ping_parser.parse(result).as_dict()

    rtt_max = resultParser(result_dict[MAX_PING])
    rtt_min = resultParser(result_dict[MIN_PING])
    rtt_avg = resultParser(result_dict[AVG_PING])
    packets_sent = result_dict[SENT]
    packets_received = result_dict[RECEIVED]
    packet_loss = result_dict[PACKET_LOSS]

    jitter = measureJitter(ping_destination)

    if jitter == NO_RESULT:
        registerPingResult(
                ping_destination, 
                round(float(rtt_max), 3), 
                round(float(rtt_min), 3), 
                round(float(rtt_avg), 3), 
                packets_sent, 
                packets_received, 
                round(float(packet_loss), 3), 
                jitter, 
                interface
            )
    else:        
        registerPingResult(
                ping_destination, 
                round(float(rtt_max), 3), 
                round(float(rtt_min), 3), 
                round(float(rtt_avg), 3), 
                packets_sent, 
                packets_received, 
                round(float(packet_loss), 3), 
                round(float(jitter), 3), 
                interface
            )

    return packet_loss

def monitorPing():
    try:
        gateways = netifaces.gateways()  
        interface = gateways['default'][netifaces.AF_INET][1]

        packet_loss = pingFromInterface(interface, 5)

        active_interfaces_count = len(gateways[2])

        if packet_loss == 100 and active_interfaces_count == 2: # try pinging with the wireless interface
            
            interface = gateways[2][1][1]        
            pingFromInterface(interface, 5)
        
        print("\x1b[6;30;42m [LOG Ping] Ping Successfully Completed\x1b[0m", flush=True)


    except Exception as e: # when the device is not connected to a network and have no IP, an exception will be thrown
        print(f"\x1b[6;30;41m [LOG Ping] An error ocurred: {str(e)}\x1b[0m", flush=True)
        registerPingResult(getDestinationIP(), 0, 0, 0, 0, 0, 0, gateways['default'][netifaces.AF_INET][1])
