#!/usr/local/bin/python
import datetime, dateutil.tz
tzl = dateutil.tz.tzlocal()
class A(datetime.datetime):
    def __init__(self, *args, **kwargs):
        if len(args) < 8 and 'tzinfo' not in kwargs:
            # kwargs['tzinfo'] = dateutil.tz.tzlocal()
            kwargs['tzinfo'] = tzl
        print ("kwargs = %s" % (kwargs))
        print ("kwargs['tzinfo'] = %s" % (repr(kwargs['tzinfo'])))
        print ("hash(kwargs['tzinfo']) = %s" % hash(repr(kwargs['tzinfo'])))
        super(A, self).__init__(*args, **kwargs)

x = datetime.datetime(2014, 07, 25, tzinfo=dateutil.tz.tzlocal())
print x.tzinfo
print "\ncalled args only"
a = A(2014, 07, 25, 1, 2, 4)
print a.tzinfo
print "\ncalled with tzinfo"
b = A(2014, 07, 25, tzinfo=tzl)
print b.tzinfo
