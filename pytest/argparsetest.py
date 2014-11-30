#!/usr/local/bin/python
import sys, os, argparse

def main(args):
    prog = os.path.basename(__file__)
    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument('--foo', nargs='?', help='foo help')
    parser.add_argument('bar', nargs='+', help='bar help')
    opts = parser.parse_args(args)
    print "Printing opts:"
    print opts
    

if __name__ == '__main__':
    main(sys.argv)

