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

# Size of the dictionary to create
size = 2000
partialSize = size / 100
iterations = 200
values = [int(random.random()*size) for i in xrange(size)]

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

def t00TestNumericListAppend():
    for x in xrange(size):
        d = []
        for i in xrange(4):
            d.append(values[i])

def t00TestNumericListInitAndSet():
    for x in xrange(size):
        d = [0] * 4
        for i in xrange(4):
            d[i] = values[i]
                
def t01dictTestIf():
   d = {}
   for i in xrange(size):
       val = values[i]
       if val not in d:
           d[val] = []
       d[val].append(i % partialSize)

# Append values to lists in a dict.  Tests how we should check if some value
# exists in a dict.
def t02dictTestIfElse():
   d = {}
   for i in xrange(size):
       val = values[i]
       if val not in d:
           d[val] = [i]
       else:
           d[val].append(i % partialSize)

def t03dictTestSetDefault():
   d = {}
   for i in xrange(size):
       val = values[i]
       d.setdefault(val, []).append(i % partialSize)

def t04dictTestInitFirst():
   d = {}
   for i in xrange(size):
       d[i] = []

   for i in xrange(size):
       d[values[i]].append(i % partialSize)

def t05dictTestInitAndClean():
   d = {}
   for i in xrange(size):
       d[i] = []

   for i in xrange(size):
       d[values[i]].append(i % partialSize)

   for i in xrange(size):
       if not d[i]:
           d.pop(i)

def t06listTestInitFirst():
   d = [[] for i in xrange(size)]

   for i in xrange(size):
       d[values[i]].append(i % partialSize)


def t07listCompTestInitFirst():
   d = [[] for i in xrange(size)]

   [d[values[i]].append(i % partialSize) for i in xrange(size)]

def t07listCompTestInitFirstIf():
   d = [[] for i in xrange(size)]

   for i in xrange(size):
       L = d[values[i]]
       token = i % partialSize
       if token not in L:
           d[values[i]].append(i % partialSize)

def t07listCompTestInitFirstSet():
   d = [set() for i in xrange(size)]

   for i in xrange(size):
       L = d[values[i]]
       token = i % partialSize
       if token not in L:
           d[values[i]].update([i % partialSize])

def t07listCompTestInitFirstThenCleanListSet():
   d = [[] for i in xrange(size)]

   for i in xrange(size):
       d[values[i]].append(i % partialSize)

   for i in xrange(size):
       val = values[i]
       d[val] = list(set(d[val]))

def t07listCompTestInitFirstThenCleanSet():
   d = [[] for i in xrange(size)]

   for i in xrange(size):
       d[values[i]].append(i % partialSize)

   for i in xrange(size):
       val = values[i]
       d[val] = set(d[val])
           
def t08listCompTestInitFirst():
   d = [[] for i in xrange(size)]

   [d[values[i]].append(i % partialSize) for i in xrange(size)]

def t09listSetTestInitFirst():
   d = [set() for i in xrange(size)]

   for i in xrange(size):
       d[values[i]].update([i % partialSize])

def t10listSetCompTestInitFirst():
   d = [set() for i in xrange(size)]

   [d[values[i]].update([i % partialSize]) for i in xrange(size)]

class Obj(object):
    def __init__(self, id, value):
        self.id = id
        self.value = value

objects = [Obj(i,value) for i,value in enumerate(values)]
objectIds = [o.id for o in objects]
objectValues = [o.value for o in objects]

def t11_simpleDictCreationTest_forLoop():
    d = {}
    for obj in objects:
        d[obj.id] = obj.value

def t11_simpleDictCreationTest_forLoopFromExistingLists():
    d = {}
    for id, value in zip(objectIds,objectValues):
        d[id] = value

def t11_simpleDictCreationTest_forLoopFromNewLists():
    objectIds = [o.id for o in objects]
    objectValues = [o.value for o in objects]
    d = {}
    for id, value in zip(objectIds,objectValues):
        d[id] = value

def t11_simpleDictCreationTest_dict():
    d = dict([(obj.id, obj.value) for obj in objects])

def t11_simpleDictCreationTest_dictFromExistingLists():
    d = dict([(id, value) for id,value in zip(objectIds, objectValues)])

def t11_simpleDictCreationTest_dictFromNewLists():
    objectIds = [o.id for o in objects]
    objectValues = [o.value for o in objects]
    d = dict([(id, value) for id,value in zip(objectIds, objectValues)])

def t12_forLoopVsIndexingTest_noIndexing():
    L = []
    for val in values:
        L.append(val)

def t12_forLoopVsIndexingTest_enumerate():
    L = []
    for i,val in enumerate(values):
        L.append(values[i])

def t12_forLoopVsIndexingTest_xrange():
    L = []
    for i in xrange(len(values)):
        L.append(values[i])

def t13_listCompVsIndexingTest_noIndexing():
    [val for val in values]


locs = locals()

funcType = type(lambda: None)

keys = locals().keys()
keys.sort()
for name in keys:
    func = locs[name]
    if "Test" in name and isinstance(func, funcType):
        with TimerContext(name):
            for i in xrange(iterations):
                func()

# with TimerContext("run cStyle test"):
#     for i in xrange(iterations):
#         cStyle(uvCoords)

# with TimerContext("run pyStyle test"):
#     for i in xrange(iterations):
#         pyStyle(uvCoords)

io.write("Done!")



