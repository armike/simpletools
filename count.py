#!/usr/local/bin/python
import time, os, sys

def main():
    for i in range(100000):
        try:
            outfile = sys.argv[1]
        except IndexError:
            outfile = "/tmp/count_output.log"
        print i
        myfile = open(outfile, "w")
        myfile.write(str(i) + "\n")
        time.sleep(1)
        
if __name__=="__main__":
    print "MAIN NAME"
    main()
    
    
