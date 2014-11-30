#!/usr/local/bin/python
normal =  '\033[0m'
for i in range(108):
    print ("%2d: \033[%dm a test string%s" % (i,i, normal))
