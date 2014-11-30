#!/usr/local/bin/python
import sys, pprint, array
from timercontext import TimerContext
arrHits = 0
arrMisses = 0

def sumLists(n):
    lists = []
    for i in range(1, n):
        lists += _sumLists(i, n)
    return lists

def _sumLists(n, remaining):
    """
    :Parameters:
        n : `int`
            The element to append to this list.  All further elements
            must be less than or equal to n.
        remaining : `int`
            The amount left to get.
    :Returns:
        List of lists of ints.
    :Rtype:
        `list list`
    """
    remaining = remaining - n
    if remaining == 0:
        return [ [n] ]
    lists = []
    for i in range(min(remaining, n), 0, -1):
        for sl in _sumLists(i, remaining):
            sl.insert(0, n)
            lists.append(sl)
    return lists

def sumListsCachedDict(n):
    lists = []
    cache = {}
    for i in range(1, n):
        lists += _sumListsCachedDict(i, n, cache)
    return lists

def _sumListsCachedDict(n, remaining, cache):
    """
    :Parameters:
        n : `int`
            The element to append to this list.  All further elements
            must be less than or equal to n.
        remaining : `int`
            The amount left to get.
    :Returns:
        List of lists of ints.
    :Rtype:
        `list list`
    """
    if n in cache and remaining in cache[n]:
        return cache[n][remaining]
    remaining = remaining - n
    if remaining == 0:
        if n not in cache:
            cache[n] = {remaining: [[n]]}
        else:
            cache[n][remaining] = [[n]]
        return [[n]]
    lists = []
    for i in range(min(remaining, n), 0, -1):
        for sl in _sumListsCachedDict(i, remaining, cache):
            lists.append([n] + sl)
    if n not in cache:
        cache[n] = {remaining: []}
    cache[n][remaining] = lists
    return lists

def sumListsCachedPyArr(n):
    lists = []
    cache = [None] * (n**2)
    for i in range(1, n):
        lists += _sumListsCachedPyArr(i, n, cache)
    return lists

def _sumListsCachedPyArr(n, remaining, cache):
    """
    :Parameters:
        n : `int`
            The element to append to this list.  All further elements
            must be less than or equal to n.
        remaining : `int`
            The amount left to get.
    :Returns:
        List of lists of ints.
    :Rtype:
        `list list`
    """
    cacheKey = n + n*remaining
    if cache[cacheKey] is not None:
        return cache[cacheKey]
    remaining = remaining - n
    if remaining == 0:
        return [[n]]
    lists = []
    for i in range(min(remaining, n), 0, -1):
        for sl in _sumListsCachedPyArr(i, remaining, cache):
            lists.append([n] + sl)
    cache[cacheKey] = lists
    return lists
    
def main(args):
    try:
        n = int(args[1])
    except:
        n = 10
        print "Couldn't read cmdline argument, using 10 for n"
    # with TimerContext("do cached arr"):
    #     sumListsCachedArr(n)
    # print "Array hits:   %d" % arrHits
    # print "Array misses: %d" % arrMisses

    # with TimerContext("do cached dict"):
    #     sumListsCachedDict(n)
    with TimerContext("do array cached"):
        sumListsCachedPyArr(n)
    with TimerContext("do uncached"):
        sumLists(n)
    

if __name__ == '__main__':
    main(sys.argv)
