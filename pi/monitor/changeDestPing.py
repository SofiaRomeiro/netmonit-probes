from monitor.configurations import Configurations
from constants import LOCAL_DB_CONNECTION_STRING

def monitorChangeDestPing(ip, configs: Configurations):
    configs.destination_ip = ip
    print("[LOG - monitorChangeDestPing()] Configs = " + configs.destination_ip)