import datetime
from enum import Enum

class TCPSegmentDirection(Enum):
    FROM_SRC_TO_DST = 0
    FROM_DST_TO_SRC = 1

class TCPSegment:
    direction = None
    def __init__(self, flags, size):
        self.flags = flags
        self.size = size
        self.timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')