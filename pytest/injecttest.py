#!/usr/local/bin/python
import timercontext

def injectFuncA():
    print "one"

def injectFuncB(blah="blah"):
    print blah

class InjectClass(object):
    def __init__(self, foo=None):
        self.foo = foo

    def injectMethod(self):
        print self.foo

    @classmethod
    def injectClassMethod(cls):
        print "in classmethod"
    

def main():
    injectFuncA()
    injectFuncB('blah')
    c = InjectClass("foo")
    c.injectMethod()
    c.injectClassMethod()
    

if __name__ == '__main__':
    timercontext.injectTimerDecoratorIntoDict(locals())
    # timercontext.injectTimerDecoratorIntoDict(globals())


    print "Executing", __file__, "-------------------------"
    main()
