#!/usr/local/bin/python
import sys, random
import numpy
from timercontext import TimerContext

class Bbox(object):
    def __init__(self):
        self.max = [random.random(), random.random(), random.random()]
        self.min = [random.random(), random.random(), random.random()]

def main():
    bbox = Bbox()
    iters = 10000
    try:
        iters = int(sys.argv[1])
    except IndexError, ValueError:
        pass
    print "Running %d iterations" % iters
    with TimerContext("calculate %d means with numpy" % iters):
        for i in range(iters):
            numpy.mean([bbox.max[0], bbox.min[0]])
            numpy.mean([bbox.max[1], bbox.min[1]])
            numpy.mean([bbox.max[2], bbox.min[2]])
    with TimerContext("calculate %d means with vanilla python" % iters):
        for i in range(iters):
            (bbox.max[0] + bbox.min[0]) / 2.0
            (bbox.max[1] + bbox.min[1]) / 2.0
            (bbox.max[2] + bbox.min[2]) / 2.0
    with TimerContext("calculate %d means overflow safe vanilla python" %
                      iters):
        for i in range(iters):
            bbox.min[0] + ((bbox.max[0] - bbox.min[0]) / 2.0)
            bbox.min[1] + ((bbox.max[1] - bbox.min[1]) / 2.0)
            bbox.min[2] + ((bbox.max[2] - bbox.min[2]) / 2.0)

        

if __name__ == '__main__':
    main()
