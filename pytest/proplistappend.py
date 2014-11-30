#!/usr/local/bin/python
class A(object):
    def __init__(self):
        self._list = None

    def lister():
        def fget(self):
            if self._list is None:
                self._list = ['an initial list']
            return self._list
        def fset(self, value):
            self._list = value
        return locals()
    lister = property(**lister())

a = A()
a.lister.append('something!')
print a.lister
