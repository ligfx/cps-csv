#!/usr/bin/env python
#coding:utf-8

import codecs
import json
import re

VARNAME = 0
SIZE = 1
DESCRIPTION = 2
STARTPOS = 3
ENDPOS = 4

def match_header(line, curpos):
	m = re.match(u"^(\w+)\s+(\d+)(\s+.*)?\s+(\d+)\s*-\s*(\d+)$", line)
	if not m:
		# sys.stderr.write("Didn't match regex\n")
		return None
	varname, size, description, startpos, endpos = m.groups()
	varname = varname.lower()
	size = int(size)
	description = (description or "").strip()
	startpos = int(startpos)
	endpos = int(endpos)

	if not startpos == curpos:
		# sys.stderr.write("Variable '%s' starts at %s, but parser is at %s\n" % (varname, startpos, curpos))
		return None
	if not (endpos - startpos) == (size - 1):
		# sys.stderr.write("Size and starting and ending position don't make sense!\n")
		return None
	return (varname, size, description, startpos, endpos)

def pretty(header, description, category):
	return {
		"varname": header[VARNAME],
		"size": header[SIZE],
		"startpos": header[STARTPOS],
		"endpos": header[ENDPOS],
		"description": (header[DESCRIPTION] + "\n" + "".join(description).strip()),
		"category": category
	}

def jsonify(data_dictionary_part, startpos, category):
	position = startpos
	variables = []
	header = None
	description = []
	for line in f:
		line = line.replace(u"\u2013", "-")
		if not header:
			header = match_header(line, position)
			if not header:
				raise Exception("Tried to match a variable header, got: %s" % line)
			position = header[ENDPOS] + 1
		else:
			if not match_header(line, position):
				description.append(line)
			else:
				variables.append(pretty(header, description, category))
				header = match_header(line, position)
				position = header[ENDPOS] + 1
				description = []
	variables.append(pretty(header, description, category))
	return variables

args = (
	("jan13-household-info.txt", 1, "household"),
	("jan13-geographic-info.txt", 89, "geographic"),
	("jan13-persons-demographic.txt", 114, "demographic"),
	("jan13-persons-laborforce.txt", 178, "laborforce")
)

doc = {
	"title": "CPS RECORD LAYOUT FOR BASIC LABOR FORCE ITEMS",
	"subtitle": "STANDARD PUBLIC USE FILES",
	"starting": "January 2013",
	"variables": []
}

for fname, startpos, category in args:
	with codecs.open(fname, encoding='utf-8') as f:
		for v in jsonify(f, startpos, category):
			doc['variables'].append(v)

print json.dumps(doc)
