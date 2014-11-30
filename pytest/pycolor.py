#!/usr/local/bin/python
import subprocess
import pygments
from pygments.lexers.agile import PythonLexer
from pygments.formatters.html import HtmlFormatter
infile = open('/home/maross/pytest/pycolor.py', 'r')
outfile = open('/tmp/out.html', 'w')
pygments.highlight(infile.read(), PythonLexer(), HtmlFormatter(full=True), outfile)
infile.close()
infile.close()
subprocess.call(['/opt/google/chrome/google-chrome',' /tmp/out.html'])
