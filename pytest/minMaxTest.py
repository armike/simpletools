#!/usr/local/bin/python

from __future__ import with_statement
import random, time, sys
import studioenv
from studio import io

class TimerContext:
    """A context to time operations.  This allows us to time code
    without having to intersperse timing lines lines everywhere, but
    comes with the price of ugly nesting.
    """
    def write(self, msg=None, startTime=None, endTime=None, color=None):
        """Write the elapsed time message.
        """
        msg = msg or self.msg
        startTime = startTime or self.startTime
        endTime = endTime or self.endTime
        endTime = endTime or time.time()
        color = color or self.color
        io.write("%s%.4f sec%s to %s" % (color,
                                        endTime-startTime,
                                        io.color.FG_GREEN, msg))        

    def reset(self, msg=None):
        """Reset this timer's start time.
        """
        msg = msg or self.msg
        self.startTime = time.time()
        self.endTime = None

    def __init__(self, msg, color=io.color.FG_BLUE):
        self.msg = msg
        self.color = color
        self.startTime = time.time()
        self.endTime = None

    def __enter__(self):
        self.startTime = time.time()

    def __exit__(self, type, value, traceback):
        self.endTime = time.time()
        self.write()


random.seed(1)

size = 200000
iterations = 200
uvCoords = [random.random() for i in xrange(size)]

# Method 1: pseudo c-style
# 

def cStyle(L):
    """
    """
    uMin = -10000
    uMax = 1000
    vMin = -10000
    vMax = 1000
    for i in xrange(0, size, 2):
        u = L[i]
        v = L[i+1]
        if uMin > u:
            uMin = u
        if uMax < u:
            uMax = u
        if vMin > v:
            vMin = v
        if vMax < v:
            vMax = v

    return uMax-uMin,vMax-vMin
                                        
    
def pyStyle(L):
    """Return the center UV coordinate of the center of this Sop.
    """
    # Get a flat list of UV coordinates
    # 
    uValues = L[::2] 
    vValues = L[1::2] 
    uMin = min(uValues)
    uMax = max(uValues)
    vMin = min(vValues)
    vMax = max(vValues)
    return (uMax-uMin, vMax-vMin)

io.write("Size: %d"  % (size))
io.write("iterations: %d" % (iterations))



with TimerContext("run cStyle test"):
    for i in xrange(iterations):
        cStyle(uvCoords)

with TimerContext("run pyStyle test"):
    for i in xrange(iterations):
        pyStyle(uvCoords)

io.write("Done!")
