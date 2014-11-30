#!/usr/local/bin/python

class PickleMe:
    def __init__(self, otherPickle=None):
        self.aString = 'this is a string'
        self.anInt = 100
        self.aFloat = 1.5
        self.aPickleMeObject = otherPickle

    def printSomething(self):
        print 'Something'

    def printSomethingElse(self):
        print 'SomethingElse'

