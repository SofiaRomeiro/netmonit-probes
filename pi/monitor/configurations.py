from datetime import datetime
from enum import Enum

class Configurations:

    destination_ip: str
    last_updated_monitor: datetime
    last_updated_external_performance: datetime
    last_updated_internal_performance: datetime
    last_updated_wifi_test: datetime
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configurations, cls).__new__(cls)
        return cls.instance


class TypeOfUpdate(Enum):
    MONITOR = 1
    EXTERNAL_PERFORMANCE = 2
    INTERNAL_PERFORMANCE = 3
    WIFI = 4

class ProtocolOfPerformanceTest(Enum):
    TCP = 1
    UDP = 2

class TypeOfPerformanceTest(Enum):
    INTERNAL = 1
    EXTERNAL = 2




    