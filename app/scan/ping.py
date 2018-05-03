import os
from enum import Enum

class PingScanResponse(Enum):
    HOST_AVAILABLE = 1
    HOST_UNAVAILABLE = 2

def ping(hostname):
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        return PingScanResponse.HOST_AVAILABLE
    else:
        return PingScanResponse.HOST_UNAVAILABLE