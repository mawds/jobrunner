#!/usr/bin/python

import sys
import re
import itertools
import unittest

class TestStringMethods(unittest.TestCase):

    def test_single_expand(self):
        self.assertListEqual(parseCommandString("a.out {1,2,3}"), \
        ['a.out 1', 'a.out 2', 'a.out 3'])
    
    def test_multi_expand(self):
        self.assertListEqual(parseCommandString("a.out {1,2,3} {x,y}"), \
        ['a.out 1 x', 'a.out 2 x', 'a.out 3 x', 'a.out 1 y', 'a.out 2 y', 'a.out 3 y'])
    
    def test_named_expand(self):
        self.assertListEqual(parseCommandString("a.out {a:1,2} {a:}"),  \
        ['a.out 1 1', 'a.out 2 2'])

    def test_multiple_named_expand(self):
        self.assertListEqual(parseCommandString("a.out {a:1,2} {b:3,4} {a:} {b:}"), \
        ['a.out 1 3 1 3', 'a.out 1 4 1 4', 'a.out 2 3 2 3', 'a.out 2 4 2 4'])

def parseGroup(groupstring):
    """Parse an extracted group; returns a list containg each option"""
    m = re.search(r"^(\w):(.*)", groupstring)
    if m:
        groupName = m.group(1)
        justgroups = m.group(2)
    else:
        groupName = next(groupNames)
        justgroups = groupstring 

    # If we've got an empty named group we don't want to overwrite it
    if len(justgroups) > 0:
        groupList = justgroups.split(",")
    else:
        groupList = None

    return (groupName, groupList)

def genGroupName():
    chars = range(ord("a"), ord("z")+1)
    pos = -1
    while pos < len(chars)-1:
        pos = pos + 1
        yield "x"+chr(chars[pos])

groupNames = genGroupName()

def parseCommandString(commandString):
    groups = dict()
    groupList = []
    commandLines = []

    # We don't really care what the options are; we're just interested in extracting all the {}s
    pattern = r'\{(.+?)\}'
    groupregex = re.compile(pattern)
    for group in groupregex.finditer(commandString):
        (groupName, groupValues) = parseGroup(group.group(1))
        if groupValues is not None:
            groups[groupName] = groupValues
        groupList.append(groupName)


    # Convert dict to a list of lists so we get the option arguments in the correct order
    masterlist = []
    masterlistnames = []
    for g in groups:
        masterlistnames.append(g)
        masterlist.append(groups[g])

    for i in itertools.product(*masterlist):
        thisCommand = commandString
        numSubs = 0
        while numSubs < len(groupList):
            thisCommand = re.sub(pattern, \
            i[masterlistnames.index(groupList[numSubs])], \
            thisCommand, count=1)
            numSubs = numSubs+1
        commandLines.append(thisCommand)

    return commandLines

if __name__ == '__main__':
    unittest.main()
