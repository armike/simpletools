#!/usr/local/bin/python

import studioenv

class MegaParent(object):
    """Nada.
    """

    def __init__(self, x):
        self.x = x
        io.write("MegaParent init")
 
class Parent(MegaParent):
    
    def __init__(self, x):
        super(Parent, self).__init__(x)
        io.write("Parent init")

    @classmethod
    def caller(cls):
        print ("-----------------------")
        print ("Parent caller!")
        try:
            cls.callee()
        except:
            pass

    @classmethod
    def callee(cls):
        print ("Parent callee!")
        
class Child(Parent):
    def __init__(self, x):
        super(Child, self).__init__(x)
        io.write("Child init")

    @classmethod
    def callee(cls):
        print ("Child callee!")

class GrandChild(Child):
    def __init__(self, x):
        io.write("GrandChild init")
        super(GrandChild, self).__init__(x)
    
    @classmethod
    def callee(cls):
        print ("GrandChild callee!")
                        

Child.caller()
GrandChild.caller()


class CallerClass:
    def call(self):
        Parent.caller()
        Child.caller()
        GrandChild.caller()


cc = CallerClass()

cc.call()

