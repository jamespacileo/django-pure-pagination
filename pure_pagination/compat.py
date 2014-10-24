import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    range = xrange
    text_type = unicode
elif PY3:
    range = range
    text_type = str
