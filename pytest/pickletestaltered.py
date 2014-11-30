#!/usr/local/bin/python

import sys, pickle, yaml
from pickleable import PickleMe

def main():
    path = '/tmp/test.pickle'
    with open(path, 'r') as f:
        L = yaml.load(f)
    print L

    L[0].printSomething()
    L[0].printSomethingElse()
    
if __name__ == '__main__':
    main()
