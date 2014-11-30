#!/usr/local/bin/python

class CachedProperty(object):
    """
    A decorator that runs the body of the method once and caches the result.
    """
    def __init__(self, func):
        self.__doc__ = func.__doc__
        self.func = func
        self.name = "_" + func.__name__
        
    def __get__(self, instance, cls):
        name = self.name
        if instance is None:
            return self
        elif name in instance.__dict__:
            return instance.__dict__[name]
        result = self.func(instance)
        instance.__dict__[name] = result
        return result

class A(object):
    
    def __init__(self, name="name of an a"):
        self.name = name

    @CachedProperty
    def fieldA(self):
        print "calling _getField method"
        return 100

    @CachedProperty
    def fieldB(self):
        print "calling _getField method"
        return 200

def main():
    a = A()
    print "a.fieldA: %s" % a.fieldA
    print "a.fieldB: %s" % a.fieldB
    print "a.fieldA: %s" % a.fieldA
    print "a.fieldB: %s" % a.fieldB
    print "a.fieldA: %s" % a.fieldA
    print "a.fieldB: %s" % a.fieldB

if __name__ == '__main__':
    main()
        

