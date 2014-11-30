import studioenv
import studio.maya
maya = studio.maya.importMaya()
import maya.cmds
import sys

def appender(x):
  if x not in sys.path:
    sys.path.insert(0, x)

appender('/home/maross/work/toolset/modeling/third_party/maya/script/mod_frameSelect')
appender('/home/maross/work/toolset/modeling/third_party/maya/script/mod_polySym')
appender('/home/maross/work/toolset/modeling/third_party/maya/script/mod_flyPaper')
appender('/home/maross/work/mod/python')

maya.cmds.file("/studio/mad3/work/maross/pants_comparison.mb", i=1)

import studio ; reload(studio)
import studio.maya ; reload(studio.maya)
import studio.maya.model ; reload(studio.maya.model)
import studio.maya.model.color ; reload(studio.maya.model.color)
import studio.maya.model.closestpt ; reload(studio.maya.model.closestpt)
import mod_polySym ; reload(mod_polySym)
import mod_flyPaper ; reload(mod_flyPaper)

fp = mod_flyPaper.FlyPaper()

verts = maya.cmds.filterExpand(sm=31)
meshes = maya.cmds.filterExpand(sm=12)

fp.wrapObjects(['m_pant'], ['m_pant1'], rayTrace=1, iterations=2)
