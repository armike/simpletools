#!/usr/local/bin/python
import sys
import traceback
import functools 

class MyWindowClass(object):
    def warn(self, message, time = 0):
        print "Warning: %s" % message
            # self.uiStatusBar.showMessage(message, msecs= time)

    def catchError(message):
        def decorator(func):
            @functools.wraps(func)
            def wrapped(self, *args, **kwargs):
                print args
                print kwargs
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    self.warn(exc_value)
                    print(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            return wrapped
        return decorator

    @catchError('Build failed! See the Python console for more info.')
    def someMethod(self):
        raise ValueError('Bad things happened')

class Object:
    def getDecorator(getDecoratorArg):
        print "in getdecorator, getDecoratorArg: %s" % getDecoratorArg
        def decorator(func):
            print "in decorator, func: %s" % func
            def method(self, *args, **kwargs):
                print "in wrapper, func: %s" % func
                self.write("Accessing self in decorated method")
                return func(self, *args, **kwargs)
            return method
        return decorator

    def write(self, msg):
        print msg

    def someMethod(self, blah):
        print "in someMethod."
    someMethod = getDecorator("blah")(someMethod)
    

def main():
    win = MyWindowClass()
    win.someMethod()
    
    obj = Object()
    obj.someMethod("something")

if __name__ == "__main__":
    main()
