#!/usr/local/bin/python

import sys, os
import studioenv
import studio.error
from studio import io

def main():
    print "Raising an error..."
    try:
        raise ValueError("This is the original message.")
    except Exception, e:
        studio.error.addToMessage(e, "This is added with addToMessage")
        studio.error.addToErrorLog(e, "This is added with addToErrorLog")
        raise

if __name__ == '__main__':
    main()
