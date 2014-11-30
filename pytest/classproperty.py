#!/usr/local/bin/python

# Result: I can't figure out how you'd have a property on a class.  Too bad.
# Ought to just make it a classmethod, I suppose.
# 
class A(object):
    counter = 0
    def prop():
        @classmethod
        def fget(cls):
            print "cls: %s" % cls
            cls.counter += 1
            return cls.counter
        return locals()
    prop = property(**prop())

print A.prop
print A.prop
print A.prop
print A.prop
