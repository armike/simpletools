#!/usr/local/bin/python
import sys,time
class Foo(object):
    def __init__(self):
        self.stackedWidget = StackedWidget()

    def funcLoop(self, iters):
        for i in xrange(iters):
            if self.stackedWidget.currentIndex() == 0:
                pass
            elif self.stackedWidget.currentIndex() == 1:
                pass

    def varLoop(self, iters):
        for i in xrange(iters):
            currentIndex = self.stackedWidget.currentIndex()
            if currentIndex == 0:
                pass
            elif currentIndex == 1:
                pass


class StackedWidget(object):
    def currentIndex(self):
        return 1
    

def doSomething():
    pass
def doSomethingElse():
    pass

def testBoth(iters):
    f = Foo()
    st = time.time()
    f.funcLoop(iters)
    et = time.time()
    print "function loop: %f" % (et-st)
    st = time.time()
    f.varLoop(iters)
    et = time.time()
    print "cached loop:   %f" % (et-st)

if __name__ == "__main__":
    try:
        iters = int(sys.argv[1])
    except (ValueError,IndexError):
        iters = 1000000
        print "Error reading sys.argv[1], using %d iterations" % iters
    testBoth(iters)
