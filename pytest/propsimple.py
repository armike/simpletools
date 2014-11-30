#!/usr/local/bin/python

class Parent(object):

    def children():
        doc = """A property created by calling property"""
        def fget(self):
            if not hasattr(self, '_children') is None:
                self._children = self.createChildren()
            return self._children
        return locals()
    children = property(**children())

    @property
    def childrenDecorated(self):
        """A property created via a decorator"""
        if not hasattr(self, '_childrenDecorated'):
            self._childrenDecorated = self.createChildren()
        return self._childrenDecorated
        
    # @childrenDecorated.setter
    # def childrenDecorated(self, value):
    #     self._childrenDecorated.append(value)

    def createChildren(self):
        return [1,2,3]

p = Parent()
print p.__dict__
print p.children
print Parent.children
print p.__dict__
print p.childrenDecorated
print p.__dict__
print Parent.childrenDecorated

