#!/usr/bin/env python
# sanity check an event
# percent between 0 and 100%
# nothing negative
from __future__ import print_function
import sys
import os
# thanks python 3.13!
try:
    from shlex import quote as cmd_quote
except ImportError:
    from pipes import quote as cmd_quote

logfile = "slog.%d" % (os.getpid())

s = "./ucevent.py -x, -o " + logfile + " " + " ".join(map(cmd_quote, sys.argv[1:]))
w = os.getenv("WRAP")
if w:
    s = w + " " + s
print(s)
r = os.system(s)
if r != 0:
    print("ucevent failed", r)
    sys.exit(1)

f = open(logfile, "r")
fields = f.readline().strip().split(",")
for l in f:
    vals = l.strip().split(",")
    for v, h in zip(vals, fields):
        if fields == "timestamp":
            continue
        try:
            num = float(v)
        except ValueError:
            print(h,v)
            continue
        if num < 0:
            print(h,"negative value",v)
        if h.find("_PCT") >= 0 or h.find("PCT_") >= 0:
            if num < 0 or num > 1.01:
                print(h,"percent out of bound", v)

os.remove(logfile)
