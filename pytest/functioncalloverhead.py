#!/usr/local/bin/python
from __future__ import with_statement
"""
Measure the overhead from making a function call.
"""

import studioenv
import sys, os, time, random
from studio import io

def main():
    curTime = int(time.time())
    daySeconds = 60 * 60 * 24
    dataSize = 1000000
    dayStart = 8 * 3600
    dayEnd = 19 * 3600
    
    times = [curTime + random.randint(curTime-daySeconds, curTime+daySeconds)
             for i in xrange(dataSize)]
    with TimerContext("check time of day without a function call"):
        a = timeOfDayCheckWithoutFunction(times, dayStart, dayEnd)
    with TimerContext("check time of day with a function call"):
        b = timeOfDayCheckWithFunction(times, dayStart, dayEnd)
    print "answers are identical: %s" % (a == b)

    with TimerContext("simple without a function call"):
        simpleWithoutFunction(times)
    with TimerContext("simple with a function call"):
        simpleWithFunction(times)

def simpleWithoutFunction(times):
    answers = []
    for t in times:
        t + 5

def simpleWithFunction(times):
    for t in times:
        plus5(t)

def plus5(x):
    return x+5

def timeOfDayCheckWithoutFunction(times, rangeStart, rangeEnd):
    answers = []
    for t in times:
        timeTuple = time.localtime(t)
        seconds = timeTuple[3] * 3600 + timeTuple[4] * 60 + timeTuple[5]
        answers.append(rangeStart < seconds < rangeEnd)
    return answers

def timeOfDayCheckWithFunction(times, rangeStart, rangeEnd):
    answers = []
    for t in times:
        answers.append(_inTimeRange(t, rangeStart, rangeEnd))
    return answers

def _inTimeRange(ptime, rangeStart, rangeEnd):
    """
    :Parameters:
        ptime : `int`
           Posix time value.
        rangeStart : `float`
           Start of range, in seconds from the start of the day.
        rangeEnd : `float`
           End of range, in seconds from the start of the day.
    :Returns:
       True if ptime occurs at a time of day between startHour and endHour,
       regardless of the day on which it occurs.  False otherwise.
    :Rtype:
        `bool`
    """
    timeTuple = time.localtime(ptime)
    seconds = timeTuple[3] * 3600 + timeTuple[4] * 60 + timeTuple[5]
    return rangeStart < seconds < rangeEnd


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

if __name__ == "__main__":
    main()
