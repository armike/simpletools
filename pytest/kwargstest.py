#!/usr/local/bin/python

def main():
    foo("arg1_input", "a second arg", "a third arg", rando='a random kwarg' )

def foo(arg1, kwarg1="kwarg1_default", *args, **kwargs):
    print "arg1: %s" % (arg1)
    print "args: %s" % (args)
    print "kwarg1: %s" % (kwarg1)
    print "kwargs: %s" % (kwargs)

if __name__ == '__main__':
    main()
