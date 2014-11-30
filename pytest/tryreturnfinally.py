#!/usr/local/bin/python
def foo():
    try:
        print "  in try..."
        return 5
    finally:
        print "  in finally block"

def main():
    print "Running foo:"
    x = foo()
    print "Done with foo!"
    print "x: %d" % (x)

if __name__ == "__main__":
    main()
