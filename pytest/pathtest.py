#!/usr/local/bin/python

import studioenv
import studio.framework.app
studio.ani
from studio.utils.path import Path
from studio.percs.item import Item

mindAni = studio.ani.Ani("/studio/mind/shdw_model/general/ANI")
croodAni = studio.ani.Ani("/studio/crood/shdw_model/general/ANI")

nonePath = Path("/studio/mind/shdw_model/general")
mindPath = Path("/studio/mind/shdw_model/general", ani=mindAni)

noneItem = Item(nonePath, mindAni)
studio.io.write("noneItem.path: %s" % noneItem.path)

mindItem = Item(mindPath, mindAni)
studio.io.write("mindItem.ani: %s" % mindItem.ani)
