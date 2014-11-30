#!/usr/local/bin/python
import sys, pickle, yaml
from pickleable import PickleMe

def main():
    p1 = PickleMe()
    p2 = PickleMe(p1)
    L = {'pickle1': p1,
         'pickle2': p2}
    prefix = '/tmp/pickle_test'
    dump(L, prefix, pickle)
    dump(L, prefix, yaml)

def dump(toDump, pathPrefix, module):
    path = "%s.%s" % (pathPrefix, module.__name__)
    with open(path, 'w') as f:
        module.dump(toDump, f)
    print "Dumped %s" % path

if __name__ == '__main__':
    main()
