#!/usr/bin/python

import sys
import re
import itertools
import unittest


class TestExpansion(unittest.TestCase):
    # TODO use assertSetEqual instead of assertListEqual since order doesn't matter

    def test_no_expand(self):
        self.assertListEqual(parseCommandString("a.out {1}"), \
        ['a.out 1'])

    def test_no_expand_named(self):
        self.assertListEqual(parseCommandString("a.out {a:1}"), \
        ['a.out 1'])

    def test_single_expand(self):
        self.assertListEqual(parseCommandString("a.out {1,2,3}"), \
        ['a.out 1', 'a.out 2', 'a.out 3'])
    
    def test_multi_expand(self):
        self.assertSetEqual(set(parseCommandString("a.out {1,2,3} {x,y}")), \
        set(['a.out 1 x', 'a.out 2 x', 'a.out 3 x', 'a.out 1 y', 'a.out 2 y', 'a.out 3 y']))
    
    def test_named_expand(self):
        self.assertListEqual(parseCommandString("a.out {a:1,2} {a:}"),  \
        ['a.out 1 1', 'a.out 2 2'])

    def test_multiple_named_expand(self):
        self.assertListEqual(parseCommandString("a.out {a:1,2} {b:3,4} {a:} {b:}"), \
        ['a.out 1 3 1 3', 'a.out 1 4 1 4', 'a.out 2 3 2 3', 'a.out 2 4 2 4'])

    def test_nested_groups(self):
        # Logically equivalent to test_multiple_named_expand
        self.assertListEqual(parseCommandString("--participant {p:P01,P02} --trackerfile /results/{a:OpenFace,Cppmt}/{p:}_front{a:}"), \
        ['--participant P01 --trackerfile /results/OpenFace/P01_frontOpenFace', \
        '--participant P02 --trackerfile /results/OpenFace/P02_frontOpenFace', \
        '--participant P01 --trackerfile /results/Cppmt/P01_frontCppmt', \
        '--participant P02 --trackerfile /results/Cppmt/P02_frontCppmt'])

    def test_repeated_groups(self):
        # Check cannot redefine a named group
        with self.assertRaises(ValueError):
            parseCommandString("a.out {a:1,2} {a:3,4}")

    def test_extgroup(self):
        cmdline = parseCommandString("a.out {a:}", [["a:1,2"]])
        self.assertListEqual(cmdline,['a.out 1', 'a.out 2'])
    
    def test_extgroup_mixed(self):
        cmdstring = parseCommandString("a.out {a:} {x,y}", [["a:1,2"]])
        self.assertListEqual(cmdstring, \
        ['a.out 1 x', 'a.out 1 y', 'a.out 2 x', 'a.out 2 y'])

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

def parseCommandString(commandString, extargs=None):
    groups = dict()
    groupList = []
    commandLines = []

    # Parse any externally passed groups
    if extargs is not None:
        for eg in extargs:
            if len(eg) != 1:
                print "External groups must be in a list of length 1"
                sys.exit()
            (groupName, groupValues) = parseGroup(eg[0])
            # if groupName in groups:
            #     raise ValueError("Cannot redefine a named group")
            groups[groupName] = groupValues

    parsedGroupNames=set() # A set to contain the group names we've parsed on the command line 
    # (These are used to check that we've not passed unused external groups in)

    # We don't really care what the options are; we're just interested in extracting all the {}s
    pattern = r'\{(.+?)\}'
    groupregex = re.compile(pattern)
    for group in groupregex.finditer(commandString):
        (groupName, groupValues) = parseGroup(group.group(1))
        parsedGroupNames.add(groupName)
        if groupValues is not None:
            if groupName in groups:
                raise ValueError("Cannot redefine a named group")
            groups[groupName] = groupValues
        groupList.append(groupName)

    # Convert dict to a list of lists so we get the option arguments in the correct order
    masterlist = []
    masterlistnames = []
    for g in groups:
        masterlistnames.append(g)
        masterlist.append(groups[g])
    if not parsedGroupNames.issubset(set(masterlistnames)):
        raise ValueError("Undefined groups were parsed")
    
    if parsedGroupNames != set(masterlistnames):
        # Have passed spare groups on the command line
        # These need to be deleted
        listfilter = [x in parsedGroupNames for x in masterlistnames ]
        sys.stderr.write("'spare' groups were passed: ")
        sparegroups = list( itertools.compress(masterlistnames,[not i for i in listfilter]))
        sys.stderr.write(" ".join(sparegroups) + "\n")

        masterlist = list(itertools.compress(masterlist,listfilter))
        masterlistnames = list( itertools.compress(masterlistnames,listfilter))

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
