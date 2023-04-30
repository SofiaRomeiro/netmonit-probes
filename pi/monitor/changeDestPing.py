from monitor.configurations import Configurations

def monitorChangeDestPing(ip, configs: Configurations):
    configs.destination_ip = ip