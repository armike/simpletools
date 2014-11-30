def testDecorator(func):
   def sayHello(self, *args, **kwargs):
      print "Hello %s" % func.__name__
      return func(self, *args, **kwargs)
   # sayHello.__doc__ = func.__doc__
   return sayHello 

class C(object):
   @testDecorator
   def __init__(self):
      """
      This is the constructor for objects of type C.
      """
      pass

