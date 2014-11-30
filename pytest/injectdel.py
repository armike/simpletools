#!/usr/local/bin/python
import studioenv
from studio import fbx

def delete(self):
    self.Destroy()
    print ("Destroy() called on %s." % self)

scene = fbx.loadScene('/usr/home/jrosen/seagullfly_1.fbx')
type(scene).__del__ = delete

def foo():
    scene = fbx.loadScene('/usr/home/jrosen/seagullfly_1.fbx')

foo()
