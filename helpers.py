import numpy as np
import time

def isPositionEqual(position_1,position_2):
    # Takes numpy.array as input
    return np.array_equal(position_1,position_2)

def isCollision(object,list_of_objects):
    # Return a boolean and the matching object from list of objects, if any
    # Loop through all objects to see if some has same position as first object
    for object_2 in list_of_objects:
        if isPositionEqual(object.position,object_2.position):
            return True, object_2
    
    return False, None # If we've come this far, no object overlaps

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

    def setUpdatePeriod(self,update_period):
        self.update_period = update_period