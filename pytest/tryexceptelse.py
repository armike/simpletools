#!/usr/local/bin/python
try:
    print "  in try..."
    raise ValueError()
except:
    print "excepted!"
else:
    print "  in else block!"

import sys
