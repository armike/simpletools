#!/usr/bin/python
import sys, os, re
import datetime
import dateutil.relativedelta

def main(args):
    args = args[1:]
    if args:
        for arg in args:
            print secToken2human(arg)
    else:
        for line in sys.stdin:
            tokens = line.split()
            for i,token in enumerate(tokens):
                try:
                    tokens[i] = secToken2human(token)
                except ValueError:
                    pass
            print " ".join(tokens)
             
def secToken2human(token):
    """
    :Parameters:
        token : `str`
            Token describing number of seconds to covert to human string
    :Returns:
        Human readable representation of time.
    :Rtype:
        `str`
    """
    match = re.match(r"(\d?\d?\d(,\d\d\d)*(\.\d+)*)([:.,]?)$",
                     token)
    if match:
        result = sec2human(float(match.groups()[0].replace(",", "")))
        if match.groups()[3]:
            result += match.groups()[3]
        return result
    else:
        return sec2human(float(token))

def sec2human(seconds):
    """
    :Parameters:
        seconds : `float`
            Float number of seconds.
    :Returns:
        Human readable representation of time.
    :Rtype:
        `str`
    """

    dtZero = datetime.datetime.fromtimestamp(0)
    dt = datetime.datetime.fromtimestamp(seconds)
    rd = dateutil.relativedelta.relativedelta(dt, dtZero)
    s = []
    if rd.years:
        s.append("%d years" % rd.years)
    if rd.months or rd.years:
        s.append("%d months" % rd.months)
    if rd.days or rd.years or rd.months:
        s.append("%d days" % rd.days)
    s.append("%02d:%02d:%02d" % (rd.hours, rd.minutes, rd.seconds))

    return ", ".join(s)

if __name__ == '__main__':
   main(sys.argv)
