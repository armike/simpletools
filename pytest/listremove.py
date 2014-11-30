#!/usr/local/bin/python


def main():
    L = ['zero', 'one', 'two', 'three', 'four', 'five']
    for i,elt in enumerate(L):
        print elt
        if elt == 'one':
            print "popping %s" % (L.pop(i))
            print "popping %s" % (L.pop(i))

if __name__ == '__main__':
    main()
