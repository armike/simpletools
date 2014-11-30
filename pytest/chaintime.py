#!/usr/local/bin/python
"""Time different methods of flattening lists into one long list"""
from __future__ import with_statement
from timercontext import TimerContext
import random, sys
import itertools
import array

random.seed(0)

# Time seems exponential.  Ouch!
# def sumTest(lists):
#     """Simply call sum()
#     """
#     if not lists:
#         return []
#     return sum(lists, [])

def chainTest(lists):
    """Simply call sum()
    """
    return [x for x in itertools.chain(*lists)]

def listFillTest(lists):
    if not lists:
        return []
    length = sum(map(len, lists))
    result = [None]*length
    i = 0
    for L in lists:
        for elt in L:
            result[i] = elt
            i += 1
    return result

def listAppendTest(lists):
    if not lists:
        return []
    result = []
    for L in lists:
        for elt in L:
            result.append(elt)
    return result

def listExtendForLoopTest(lists):
    if not lists:
        return []
    result = []
    for L in lists:
        result.extend(L)
    return result

def listExtendMapTest(lists):
    if not lists:
        return []
    result = []
    map(lambda L: result.extend(L), lists)
    return result

def listExtendListCompTest(lists):
    if not lists:
        return []
    result = []
    [result.extend(L) for L in lists]
    return result

def arraySignedIntSetTest(lists):
    if not lists:
        return []
    length = sum(map(len, lists))
    initializer = [0]*length
    arr = array.array('i', initializer)
    i = 0
    for L in lists:
        for elt in L:
            arr[i] = elt
            i += 1
    return list(arr)

def arraySignedLongSetTest(lists):
    if not lists:
        return []    
    length = sum(map(len, lists))
    initializer = [0]*length
    arr = array.array('l', initializer)
    i = 0
    for L in lists:
        for elt in L:
            arr[i] = elt
            i += 1
    return list(arr)

def main():
    globals_ = globals()
    keys = sorted(globals_.keys())
    size = 1000
    iterations = 10
    funcType = type(lambda:())
    print ("Size: %d"  % (size))
    print ("iterations: %d" % (iterations))
    values = [int(random.random()*size) for i in xrange(size)]
    lists = [[i]*v for i,v in enumerate(values)]
    with TimerContext("build flattened list from scratch."):
        lengths = sum(values)
        compIndex = 0
        comparison = [None]*lengths
        for i,v in enumerate(values):
            for x in range(v):
                comparison[compIndex] = i
                compIndex += 1
    for name in keys:
        func = globals_[name]
        if "Test" in name and isinstance(func, funcType):
            listsCopy = lists[:]
            with TimerContext("run %s" % (name)):
                for i in xrange(iterations):
                    result = func(listsCopy)
            if result != comparison:
                print ("comparison = %s" % (comparison))
                print ("result =     %s" % (result))
                print "%s did not match the expected result" %name
    print ("Done!")



if __name__ == '__main__':
    main()
