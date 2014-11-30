#!/usr/local/bin/python
"""
Test how retrieving class fields via self.__class__ and self behaves.
"""
class Parent(object):
    field = 'Parent field'
    
    def foo(self):
        print "from Parent"
        print "self.field: %s" % self.field
        print "self.__class__.field: %s" % (self.__class__.field)

    @classmethod
    def classFoo(cls):
        print "from Parent"
        print "cls.field: %s" % cls.field

class Child(Parent):
    field = 'Child field'

    def foo(self):
        print "in Child"
        super(Child, self).foo()
        print "from Child"
        print "self.field: %s" % self.field
        print "self.__class__.field: %s" % (self.__class__.field)
        
    @classmethod
    def classFoo(cls):
        print "in Child"
        super(Child, cls).classFoo()
        print "from Child"
        print "cls.field: %s" % cls.field

def main():
    c = Child()
    print "-- foo() -----------------"
    c.foo()
    
    print "\n-- classFoo() -----------"
    c.classFoo()

if __name__ == '__main__':
    main()
