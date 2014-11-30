#!/usr/local/bin/python
import studioenv

def main():
    aString = "blah!"
    print aString
    # import ipdb; ipdb.set_trace()
    
    print "after ipdb!"
    raise ValueError("a test error")
    

if __name__ == "__main__":
    main()
