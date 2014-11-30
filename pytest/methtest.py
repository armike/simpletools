#!/usr/local/bin/python

class A():
    def __init__(self):
        self.x = "x value!"
    
    def a(self, one, *args):
        print 'one: %s' % str(one)
        print 'a'
        print 'args: %s' (args)
        print str(*args)

    def b(self):
        print self.x

a = A()

print "a.a():"

print "getattr(a, 'a')(2, 3, 4, 5)"
getattr(a, 'a')(2)

getattr(a, 'b')()
    
