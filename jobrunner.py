""" Run a program multiple times, sweeping over a range of options """
#!/bin/python

import sys
import re

def parseGroup(groupstring):
    """Parse an extracted group; returns a list containg each option"""
    m= re.search(r"^(\w):(.+)", groupstring)
    
    if m:
        groupName = m.group(1)
        justgroups = m.group(2)

    else:
        groupName = next(groupNames)
        justgroups = groupstring 
     
    groupList = justgroups.split(",")

    return (groupName, groupList)

def genGroupName():
    chars = range(ord("a"), ord("z")+1)
    pos = -1
    while pos < len(chars)-1:
        pos = pos + 1
        yield "x"+chr(chars[pos])

groupNames = genGroupName()

if len(sys.argv) != 2:
    print "The command to be run, and its options must be passed as a quoted string"
    sys.exit()

commandString = sys.argv[1]

print commandString
groups = dict()

# We don't really care what the options are; we're just interested in extracting all the {}s
pattern = r'\{(.+?)\}'
groupregex = re.compile(pattern)
for group in groupregex.finditer(commandString):
    (groupName, groupList) = parseGroup(group.group(1))
    groups[groupName] = groupList
    
for g in groups:
    print g, groups[g]