#!/usr/local/bin/python

class A(object):
    def _foo(self):
        print "original"

class B(A):
    def _foo(self):
        super(B, self)._foo()
        print "new"

B()._foo()
