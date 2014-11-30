#!/usr/local/bin/python
def foo():
    try:
        print "  In try..."
        raise Exception("An intentional exception")
        return 5
    except:
        print "  In except block.  An exception occurred."
    finally:
        print "  In finally block"

def main():
    print "Running foo:"
    x = foo()
    print "Done with foo!"
    print "x: %s" % (x)

if __name__ == "__main__":
    main()
