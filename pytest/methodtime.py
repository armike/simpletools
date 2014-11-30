#!/usr/local/bin/python
import sys
from timercontext import TimerContext

class Cls(object):

    def run(self, iters):
        with TimerContext("run inline"):
            for i in range(iters):
                pass
        with TimerContext("run with no args"):
            for i in range(iters):
                self.noop()
        with TimerContext("run with one arg"):
            for i in range(iters):
                self.noopOneArg(0)
        with TimerContext("run with ten args"):
            for i in range(iters):
                self.noopTenArgs(0,1,2,3,4,5,6,7,8,9)

        for func,args,kwargs in [
            (self.noop, [], {}),
            (self.noopOneArg, [1], {}),
            (self.noopTenArgs, [0,1,2,3,4,5,6,7,8,9], {}),
            (self.noopHundredArgs, [x for x in range(100)], {})
            ]:
            with TimerContext("run %s" % func.__name__):
                for i in range(iters):
                    func(*args)

    def doNoop(self, func, iters):
        for i in range(iters):
            self._noop()

    def noop(self):
        pass

    def noopOneArg(self, a):
        pass

    def noopTenArgs(self, a,b,c,d,e,f,g,h,i,j):
        pass

    def noopHundredArgs(self, _0, _1, _2, _3, _4, _5, _6, _7, _8, _9,
                        _10, _11, _12, _13, _14, _15, _16, _17, _18, _19,
                        _20, _21, _22, _23, _24, _25, _26, _27, _28, _29,
                        _30, _31, _32, _33, _34, _35, _36, _37, _38, _39,
                        _40, _41, _42, _43, _44, _45, _46, _47, _48, _49,
                        _50, _51, _52, _53, _54, _55, _56, _57, _58, _59,
                        _60, _61, _62, _63, _64, _65, _66, _67, _68, _69,
                        _70, _71, _72, _73, _74, _75, _76, _77, _78, _79,
                        _80, _81, _82, _83, _84, _85, _86, _87, _88, _89,
                        _90, _91, _92, _93, _94, _95, _96, _97, _98, _99):
        pass

def main():
    obj = Cls()
    try:
        iters = int(sys.argv[1])
    except IndexError, ValueError:
        iters = 100000
    print "Running with %d iterations" % iters
    obj.run(iters)

if __name__ == '__main__':
    main()
