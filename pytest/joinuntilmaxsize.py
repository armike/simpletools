#!/usr/local/bin/python
import random
from timercontext import TimerContext

random.seed(0)

def joinUntilMaxSizePlus(L, joiner, limit):
    """
    :Parameters:
        L : `strList`
            List of strings to join
        joiner : `str`
            Join elements of L with this string.
    :Returns:
        The strings created by joining the elements of L with joiner,
        where the size of each joined string is less than limit.
    :Rtype:
        `str list`
    """
    if len(L) == 0:
        return []
    
    results = []
    s = L[0]
    for elt in L[1:]:
        if len(s + joiner + elt) > limit:
            results.append(s)
            s = elt 
        else:
            s = s + joiner + elt
    results.append(s)
    return results

def joinUntilMaxSizeFormat(L, joiner, limit):
    """Uses format operator instead of plus."""
    if len(L) == 0:
        return []
    
    results = []
    s = L[0]
    for elt in L[1:]:
        if len(s + joiner + elt) > limit:
            results.append(s)
            s = elt 
        else:
            s = "%s%s%s" % (s, joiner, elt)
    results.append(s)
    return results

numStrings = 200
joiner = ","
limit = 8191
stringLists = []
innerIterations = 100
outerIterations = 1000

for _ in xrange(innerIterations):
    stringLists.append([chr(random.randint(32, 126)) * random.randint(1,20)
                        for _ in xrange(numStrings)])

def joinPlusTest():
    for i in xrange(innerIterations):
        joinUntilMaxSizePlus(stringLists[i], joiner, limit)

def joinFormatTest():
    for i in xrange(innerIterations):
        joinUntilMaxSizeFormat(stringLists[i], joiner, limit)
    


locs = locals()
keys = locs.keys()
keys.sort()
funcType = type(lambda:None)
for name in keys:
    func = locs[name]
    if "Test" in name and isinstance(func, funcType):
        with TimerContext(name):
            for i in xrange(outerIterations):
                func()
