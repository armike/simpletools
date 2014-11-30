#!/usr/local/bin/python
import sys

def write(msg, newline=True):
    """
    :Parameters:
        msg : `str`
    """
    sys.stdout.write(msg + "\n")

def writeDict(d):        
    """
    :Parameters:
        d : `dict`
            Print d as clearly as possible.
    """
    io.write("{")
    for key,value in d.items():
        writeEntry(key,value, "")
    io.write("}")

def writeEntry(key, value, indent):
    sys.stdout.write("%s%s : " % (indent, repr(key)))
    if isinstance(value, dict):
        io.write("{")
        newIndent = indent + "    "
        for key,value in value.items():
            writeEntry(key, value, newIndent)
        io.write("%s}," % (newIndent))
    else:
        io.write("%s," % (repr(value)))
