import numpy as np
import time

def isPositionEqual(position_1,position_2):
    # Takes numpy.array as input
    return np.array_equal(position_1,position_2)

# Classes
class TimeToUpdate():
    # Takes an update period. Call function isTimeToUpdate. It returns true every time that period has passed.
    # All units are in seconds.

    last_update_time = None
    update_period = float(0)

    def __init__(self,update_period):
        self.update_period = update_period

    def isInitialized(self):
        return self.last_update_time is not None

    def isTimeToUpdate(self):
        now = time.perf_counter() # To use the same value throughout this function
        # Return true if object has never been updated
        if (not self.isInitialized() or 
                now >= self.last_update_time + self.update_period):
            self.last_update_time = now
            return True
        else:
            return False
