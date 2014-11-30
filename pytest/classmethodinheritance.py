#!/usr/local/bin/python

class ChildA(object): pass
class ChildB(object): pass
class ChildC(object): pass

class Parent(object):
    @classmethod
    def childClasses(cls):
        return [ChildA, ChildB]

class Parent2(Parent):
    @classmethod
    def childClasses(cls):
        return super(Parent2, cls).childClasses() + [ChildC]

print Parent2.childClasses()

