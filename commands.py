from enum import Enum

class Command(Enum):
    STATUS = "status"
    START = "start"
    STOP = "stop"
    RELOAD_CONFIG = "reload-config"
    SHUTDOWN = "shutdown"
