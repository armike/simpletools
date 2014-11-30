#!/usr/local/bin/python

import shlex, subprocess
options = "-foo -skip_geometry 'mm ms' -bar"
parts = shlex.split(options)
if '-skip_geometry' in parts:
    index = parts.index('-skip_geometry')
    parts[index+1] += " some other thing"
print subprocess.list2cmdline(parts)
