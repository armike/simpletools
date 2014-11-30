#!/usr/local/bin/python
from inspect import stack

class Message(object):
    @classmethod
    def format(cls, formatClass, argA, argB, kwargA='kwargA_value', kwargB='kwargB_value'):
        print "in Message.format(...)"
        format.arbitraryMessage(argA, argB, kwargA=kwargA, kwargB=kwargB)
        import pdb; pdb.set_trace()

def Format(object):

    def _wrap(self, *args, **kwargs):
        print "in Format._wrap(...)"
        import pdb; pdb.set_trace()

    def __getattr__(self, *args, **kwargs):
        print "in __getattr__"
        import pdb; pdb.set_trace()
        self._wrap
    
def main():
    foo = Message()
    foo.format(Format, 'a_value', 'b_value')

if __name__ == "__main__":
    main()
