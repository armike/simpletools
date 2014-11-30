#!/usr/local/bin/python
import re

titles = ["changes for PIPE-12153 - MAYA wrapper and maya_crash_mailer", "Adding support for vdev shots - SHADOWSTD-2228", "LAYOUT-4452 - fixes/works around maya 2012 python issue with reset()-ing QSortProxyFilterModel plus removed redundant signal-slot connections", "Promoting Matt's fix from TURBOTD-3035"]

for title in titles:
    match = re.search(r"([A-Z0-9][A-Z0-9]+-[0-9]+)", title)
    if match:
        matchString = match.groups()[0]
    else:
        match = "no match found!"
    print "%s: %s" % (matchString, title)

