#!/usr/local/bin/python
import sys

def main(args):
    try:
        n = int(args[1])
    except:
        n = 10
    for i in fibg(n):
        print i,

def fibg(end):
    a = 0
    b = 1
    while b < end:
        yield b
        a, b = b, a+b

if __name__ == '__main__':
    main(sys.argv)
