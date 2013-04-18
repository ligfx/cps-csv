#!/usr/bin/env python

import json
import sys
from io import open as open

with open("jan13dd.json") as f:
	dd = json.load(f)

out = sys.stdout

out.write(",".join(v['varname'] for v in dd['variables']))
out.write("\n")

sizes = [v['size'] for v in dd['variables']]

with open("mar13pub.dat","rb") as f:
	while True:
		out.write(",".join(f.read(s) for s in sizes))
		n = f.read(1)
		if n == "":
			exit()
		elif n == "\n":
			out.write("\n")
		else:
			raise Exception, "expected line break, got '%s'" % n
		if f.peek(1) == "":
			exit()
