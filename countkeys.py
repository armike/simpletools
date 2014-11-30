#!/usr/local/bin/python

import sys,os

def main(args):
   args = args[1:]
   if args:
      for arg in args:
          countTokens(" ".join(args))
   else:
      for line in sys.stdin:
          countTokens(line)

def countTokens(line):
    tokenCount = 0
    counterLine = [" " for i in line]
    inSpace = True
    for i,char in enumerate(line):
        if char == " ":
            inSpace = True
        else:
            if inSpace:
                counterLine[i] = str(tokenCount)
                tokenCount += 1
            inSpace = False

    for i, chars in enumerate(counterLine):
        for offset in range(1, len(chars)):
            if i+offset < len(counterLine):
                counterLine[i+offset] = ""
    print line.rstrip()
    print "".join(counterLine)
            
if __name__ == '__main__':
   main(sys.argv)
