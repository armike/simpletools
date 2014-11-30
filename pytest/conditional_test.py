#!/usr/local/bin/python
class A:
    def __init__(self):
        self.var = "nothing run"
    def foo(self):
        self.var = "foo run"
        return True
    def bar(self):
        self.var = "bar run"
        return True
   
a = A()    
x = a.foo() or a.bar()
print a.var

a = A()    
x = a.foo() and a.bar()
print a.var
