from datetime import datetime
from enum import Enum

class Configurations:

    destination_ip: str
    last_updated_monitor: datetime
    last_updated_performance: datetime
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configurations, cls).__new__(cls)
        return cls.instance


class TypeOfUpdate(Enum):
    MONITOR = 1
    PERFORMANCE = 2


    