#!/usr/local/bin/python

class Parent(object):
    def foo(self):
        print "I'm in Parent"

class Child(Parent):
    def foo(self):
        super(Child, self).foo()
        print "I'm in child"

child = Child()
child.foo()
