#!/usr/local/bin/python
import time, math
def main():
    # st = time.time( )
    # x, xx = getLargestPalindrome(15)
    # et = time.time()
    # print ("%d^2 = %d" % (x, xx))
    # print "%.2fs to find it"
    for i in range(20):
        print "%3s: %10s %10s" % (i, toBase(i, 2), toBase(i, 3))

def toBase(num, base):
    """
    :Parameters:
        num : `int`
            An integer in base 10
        base : `base`
            The base to represent num in.
    :Returns:
        $num represented in base $base
    :Rtype:
        `str`
    """
    if num <= 0:
        return "only positive nonzero numbers for now..."
    answer = ""
    tmp = num
    exponent = math.ceil(math.log(num, base))
    while exponent >= 0:
        # The value of this digit. (e.g. 1: 1, 2: 10, 3: 100 in base 10)
        # 
        digitPlace = int(base**exponent)
        
        digitValue = int(tmp / digitPlace)
        answer += str(digitValue)
        tmp -= digitValue * digitPlace
        exponent -= 1
    return answer

def getLargestPalindrome(length):
    
    x = 10**(length/2)
    xx = x**2
    largestX = 0
    largestXX = 0
    strxx = str(xx)

    while len(strxx) < 16:
        if len(strxx) == 15 and strxx[::-1] == strxx: # isPalindrome(xx):
            largestX = x
            largestXX = xx
        x += 1
        xx = x**2
        strxx = str(xx)
    return largestX, largestXX
        
def isPalindrome(x):
    strx = str(x)
    return strx == strx[::-1]

if __name__ == '__main__':
    main()
