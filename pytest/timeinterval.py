#!/usr/local/bin/python
import sys,time
import studioenv
from studio import io

def inInterval(ptime, start, end):
    """
    :Parameters:
        ptime : `int`
            posixTime
        start : `float`
            hour of day in local time that ptime should occur after
        end : `float`
            hour of day in local time that ptime should occur before
    :Returns:
        True if start < timeOfDay(ptime) < end
    :Rtype:
        `bool`
    """
    daySeconds = localDayTime(ptime)
    # localStart = start * 3600
    # localEnd   = end * 3600
    # return localStart < daySeconds < localEnd
    return start < daySeconds < end

def localDayTime(ptime):
    tup = time.localtime(ptime)
    return tup[3] * 3600 + tup[4] * 60 + tup[5]

def testDay(interval=3600, start=9, end=18):
    """
    Test every <interval>th second of the day
    """
    st = time.time()
    num = 10000
    counter = 0
    start = 3600 * start
    end = 3600 * end
    for i in xrange(num):
        for t in xrange(1, 86400, interval):
            counter += 1
            timeTuple = time.localtime(t)
            msg = time.strftime("%Y-%m-%d %H:%M:%S (%a %b %d)", timeTuple)
            result = inInterval(t, start, end)
            # color = io.color.FG_GREEN if result else io.color.FG_RED
            # msg += "%s%s: %s%s" % (color, msg, result, io.color.NORMAL)
            # io.write(msg)
    et = time.time()
    io.write("took %.2f seconds for %d checks" % (et-st, counter))
testDay()
