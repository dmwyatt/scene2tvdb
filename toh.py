#!/usr/bin/python
import glob
import sys
import os
import shutil
import re
import autoProcessTV

print "Arguments:"
for x in range(len(sys.argv)):
	print sys.argv[x]
	
if len(sys.argv) < 2:
	print "No folder supplied "
	sys.exit()

print "moving:"
print sys.argv[1]
print "-----------------------"
print
root, folder = os.path.split(sys.argv[1])
print "Root: " + root
print "Folder: " + folder
print "-----------------------"
print
try:
	id = re.search(r"\d\d\d\d", folder).group()
	fixed_season = "S" + str(int(id[:2])+2) + "E" + id[2:]
	print "Used primary id method"
	print "Fixed season/episode: " + fixed_season
except AttributeError, err:
	_id = re.search(r"S(\d\d)E(\d\d)", folder).groups()
	id = re.search(r"S\d\dE\d\d", folder).group()
	season = int(_id[0])
	ep = _id[1]
	fixed_season = "S"+ str(season+2) + "E" + ep
	print "Used secondary id method"
	print "Fixed season/episode: " + fixed_season

print "-----------------------"
print

new_folder = os.path.join(root, folder.replace(id, fixed_season))
new_folder = new_folder.replace("program", "")
new_folder = new_folder.replace("Program", "")

print "---------------------"
print
print "to: " + new_folder
print
shutil.move(sys.argv[1], new_folder)

files = os.listdir(new_folder)
print "files: " + str(files)

for f in files:

	if id in f:
		full_path = os.path.join(new_folder, f)
		if os.path.isfile(full_path):
			new_f = f.replace(id, fixed_season)
			new_f = new_f.replace("program", "")
			new_f = new_f.replace("Program", "")
			shutil.move(full_path, os.path.join(new_folder, new_f))
			print f + " renamed to: " + new_f


autoProcessTV.processEpisode(new_folder)
