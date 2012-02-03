#!/usr/bin/python
import glob
import sys
import os
import shutil
import re
import autoProcessTV

##########CONFIG############
season_delta = 2 # use positive or negative integers to add or subtract from the downloaded season number
episode_delta = 0 # use positive or negative integers to add or subtract from the downloaded episode number

# a dictionary where each key is a string in the downloaded file/folder name and the value is 
# what you want to replace the key with.  CASE SENSITIVE
# If you want to remove a string set the value to ""
replace_words = {"program": "", 
                "stupid string": "non stupid string",
                "another stupid string": "another non-stupid string"} 

# test_mode: set to True if you don't want the script to actually move anything or call sickbeard
#  In this mode will just print what it would do if it wasn't in test mode
test_mode = False 
########END CONFIG##########
                
def string_replace(orig_string):
    """ Takes the global replace_words dictionary and does all the replacements on orig_string"""
    for replace_word in replace_words:
        case_insensitive = re.compile(re.escape(replace_word), re.IGNORECASE)
        print "Replacing %s with %s" % (re.escape(replace_word), replace_words[replace_word])
        orig_string = case_insensitive.sub(replace_words[replace_word], orig_string)
        print orig_string
    return orig_string.strip()

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
    # Some episodes are labeled with season/episode like 0421
    
    # Get the four-digit season/episode id
    id = re.search(r"\d\d\d\d", folder).group()
    
    # Create the fixed S04E21-style id
    fixed_season = "S" + str(int(id[:2]) + season_delta) + "E" + int(id[2:]) + episode_delta
    print "Used primary id method"
    print "Fixed season/episode: " + fixed_season
except AttributeError, err:
    # Some episodes are labeled with S04E21
    
    # Get the S04E21-style id with season and episode groups
    _id = re.search(r"S(\d\d)E(\d\d)", folder).groups()
    
    # Get the whole string
    id = re.search(r"S\d\dE\d\d", folder).group()
    
    # Create the fixed S04E21-style id
    season = int(_id[0]) + season_delta
    ep = int(_id[1]) + episode_delta
    fixed_season = "S"+ season + "E" + ep
    print "Used secondary id method"
    print "Fixed season/episode: " + fixed_season

print "-----------------------"
print

# Replace the season/episode id in the folder name
new_folder = os.path.join(root, folder.replace(id, fixed_season))

# Replace strings in folder name
new_folder = string_replace(new_folder)

print "---------------------"
print
print "to: " + new_folder
print

if not test_mode:
    shutil.move(sys.argv[1], new_folder)

files = os.listdir(new_folder)
print "files: " + str(files)

for f in files:

    if id in f:
        full_path = os.path.join(new_folder, f)
        if os.path.isfile(full_path):
            # replace the season/episode id in the filename
            new_f = f.replace(id, fixed_season)
            # do word replacements
            new_f = string_replace(new_f)
            if not test_mode:
                shutil.move(full_path, os.path.join(new_folder, new_f))
            print f + " renamed to: " + new_f

# pass fixed file/folder to sickbeard
if not test_mode:
    autoProcessTV.processEpisode(new_folder)
