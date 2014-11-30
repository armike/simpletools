#!/usr/local/bin/python

from __future__ import with_statement
import studioenv

import datetime,yaml,json,nonexistantmodule
from studio import io
import sys, os


class TimerContext(object):
    """A context to time operations.  This allows us to time code without
    having to intersperse timing lines lines everywhere, but comes with the
    price of ugly nesting.
    """
    log = []

    def write(self, msg=None, startTime=None, endTime=None, color=None):
        """Write the elapsed time message.
        """
        msg = msg or self.msg
        startTime = startTime or self.startTime
        endTime = endTime or self.endTime
        endTime = endTime or time.time()
        color = color or self.color
        io.write("%s%.2f sec%s to %s" % (color,
                                        endTime-startTime,
                                        io.color.FG_MAGENTA, msg))
        TimerContext.log.append("%s%.2f sec%s to %s" % (color,
                                                        endTime-startTime,
                                                        io.color.FG_MAGENTA,
                                                        msg))

    def reset(self, msg=None):
        """Reset this timer's start time.
        """
        msg = msg or self.msg
        self.startTime = time.time()
        self.endTime = None

    def __init__(self, msg, color=io.color.FG_CYAN):
        self.msg = msg
        self.color = color
        self.startTime = time.time()
        self.endTime = None

    def __enter__(self):
        self.startTime = time.time()

    def __exit__(self, type, value, traceback):
        self.endTime = time.time()
        self.write()


x = 5


def foo(an_unused_param):
    an_unused_variable = 5
    x = a_variable_that_does_not_exist
    with TimerContext("nothing") as x:
        print 5
    with TimerContext("nothing"):
        print 5

def debuggers():
    import pdb; pdb.set_trace()
    import rpdb2; rpdb2.start_embedded_debugger('a')
    import pydevd ; pydevd.settrace(stdoutToServer=True, stderrToServer=True, suspend=True)
