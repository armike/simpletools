#!/usr/local/bin/python
from __future__ import with_statement
import random, time, sys
import studioenv
from studio import io
import functools

class TimerContext:
    """A context to time operations.  This allows us to time code
    without having to intersperse timing lines lines everywhere, but
    comes with the price of ugly nesting.
    """
    allTimers = []
    indentLevel = 0

    @classmethod
    def incrIndent(cls):
        cls.indentLevel += 2

    @classmethod
    def decrIndent(cls):
        cls.indentLevel -= 2

    def write(self, msg=None, startTime=None, endTime=None, color=None):
        """Write the elapsed time message.
        """
        msg = msg or self.msg
        startTime = startTime or self.startTime
        endTime = endTime or self.endTime
        endTime = endTime or time.time()
        color = color or self.color
        elapsed = endTime - startTime
        io.write("%s%.4f sec%s to %s" % (color, elapsed, io.color.FG_GREEN, msg))
        self.writtenTimes.append(("%.4f sec to %s" % (elapsed, msg), elapsed))

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
        self.writtenTimes = []
        self.__class__.allTimers.append(self)

    def __enter__(self):
        self.startTime = time.time()

    def __exit__(self, type, value, traceback):
        self.endTime = time.time()
        self.write()

    @classmethod
    def printLog(cls, sortLog=True, cutoff=0.1):
        print "TimerContext log.  Ignoring times < %f" % (cutoff)
        def writtenTimeSortKey(writtenTime):
            return writtenTime[1]
        def logSortKey(log):
            if not log.writtenTimes:
                return 0
            return sorted(log.writtenTimes, key=writtenTimeSortKey)[0]

        if sortLog:
            timers = sorted(cls.allTimers, key=logSortKey)
        else:
            timers = cls.allTimers
        for timer in timers:
            if sortLog:
                writtenTimes = sorted(timer.writtenTimes, key=writtenTimeSortKey)
            else:
                writtenTimes = timer.writtenTimes
            for writtenTime in writtenTimes:
                if writtenTime[1] > cutoff:
                    print writtenTime[0]
            

def timed(func):
    """Decorator to make an entire function one chunk in undo history.
    """
    @functools.wraps(func)
    def timedFunctionFunc(*args, **kwargs):
        funcName = "unknown function"
        fileName = "unknown file"
        try:
            funcName = func.func_code.co_name
            fileName = func.func_globals['__file__']
        except:
            pass
        # msg = "run %s() in %s\n  args: %s\n  kwargs: %s" % (funcName, fileName, args, kwargs)
        funcName = " "*TimerContext.indentLevel + funcName
        msg = "run %-50s %s" % (funcName, fileName)
        TimerContext.incrIndent()
        try:
            with TimerContext(msg):
                return func(*args, **kwargs)
        finally:
            TimerContext.decrIndent()
    return timedFunctionFunc

def injectTimerDecorator(filepath):
    """
    I've crashed python with this, so use with caution.  Best to run this
    before anything gets instantiated...

    :Parameters:
        filepath : `str`
            The file containing the module to inject into. 
            This method compares the given filepath against the __file__
            attribute of each module in sys.modules to determine what module
            to hack.  For instance, module foo should call
            injectTimerDecorator(__file__) to decorate all the functions and
            methods in itself.
    """
    print "method commented"
    # funcType = type(timed)
    # classType = type(TestClass)
    # tc = TestClass()
    # methodType = type(tc.testMethod)
    # classMethodType = type(tc.testClassMethod)
    # methodType = type(TestClass.testMethod)
    # classMethodType = type(TestClass.testClassMethod)
    # print ("funcType = %s" % (funcType))
    # print ("classType = %s" % (classType))
    # print ("methodType = %s" % (methodType))
    # print ("classMethodType = %s" % (classMethodType))
    # targets = globals()
    # for module in sys.modules:
    #     if hasattr(module, '__file__'):
    #         if module.__file__ == filepath:
    #             print "injecting into module %s" % module
    #             targets = module.__dict__
    #             break
    # else:
    #     print "injecting into globals()"
    # for name,obj in targets.items():
    #     # print "Examining %s: %s, type %s" % (name, obj, type(obj))
    #     if isinstance(obj, funcType) and obj != timed:
    #         print "rejiggering %s: %s type %s" % (name, obj, type(obj), )
    #         globals()[name] = timed(obj)
    #     if isinstance(obj, classType) and obj != TimerContext:
    #         for fieldName,fieldObj in obj.__dict__.items():
    #             print "Examining %s: %s, type %s" % (fieldName, fieldObj, type(fieldObj))
    #             if isinstance(fieldObj, methodType):
    #                 print "rejiggering %s %s: %s" % (name, obj, type(fieldObj))
    #                 obj.__dict__[fieldName]
    #             if isinstance(fieldObj, classMethodType):
    #                 print "rejiggering %s %s: %s" % (name, obj, type(fieldObj))
    #                 obj.__dict__[fieldName]

def injectTimerDecoratorIntoDict(targets):
    """
    I've crashed python with this, so use with caution.  Best to run this
    before anything gets instantiated...

    :Parameters:
        targets : `dict`
           globals()?  locals()?
    """
    
    funcType = type(timed)
    classType = type(TestClass)
    tc = TestClass()
    methodType = type(tc.testMethod)
    classMethodType = type(tc.testClassMethod)
    methodType = type(TestClass.testMethod)
    classMethodType = type(TestClass.testClassMethod)
    print ("funcType = %s" % (funcType))
    print ("classType = %s" % (classType))
    print ("methodType = %s" % (methodType))
    print ("classMethodType = %s" % (classMethodType))

    for name,obj in targets.items():

        print "Examining %s: %s, type %s" % (name, obj, type(obj))

        if isinstance(obj, funcType) and obj != timed:
            print "rejiggering %s: %s type %s" % (name, obj, type(obj), )
            globals()[name] = timed(obj)

        if isinstance(obj, (classType, type)) and obj != TimerContext:
            for fieldName in obj.__dict__:
                func = getattr(obj, fieldName)
                print "Examining %s: %s, %s" % (obj, fieldName, func)
                if callable(func):
                    try:
                        if func.im_func.func_code.co_varnames[0] == 'cls':
                            continue
                    except (AttributeError, IndexError):
                        pass
                    print "rejiggering %s %s: %s, type %s" % (obj, fieldName, func, type(func))
                    setattr(obj, fieldName, timed(func))


def _test():
    print "inside test"
    time.sleep(random.random())

class TestClass():
    def testMethod(self):
        print "testMethod"

    @classmethod
    def testClassMethod(cls):
        print "testClassMethod"

def test():
    # injectTimerDecorator()
    # _test()
    # _test()
    # _test()
    # tc = TestClass()
    # tc.testMethod()
    # tc.testClassMethod()
    # TimerContext.printLog()
    # with TimerContext("sleep a little."):
    #     time.sleep(2)
    pass

if __name__ == '__main__':
    test()
    pass
