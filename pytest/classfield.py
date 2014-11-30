#!/usr/local/bin/python

class A(object):
    classDict = {}
    
    @classmethod
    def classSet(cls, key, val):
        cls.classDict[key] = val

    def instSet(self, key, val):
        self.classDict[key] = val

def main():
    a = A()
    print "classDict: %s" % a.classDict
    a.classSet('classSet Key', 'classSet Value')
    print "classDict: %s" % a.classDict
    a.instSet('instSet Key', 'instSet Value')
    print "classDict: %s" % a.classDict
    a.classSet('classSet Key Again', 'classSet Value Again')
    print "classDict: %s" % a.classDict
    a.instSet('instSet Key Again', 'instSet Value Again')
    print "classDict: %s" % a.classDict
    

if __name__ == "__main__":
    main()
