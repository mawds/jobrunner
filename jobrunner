#! /usr/bin/env python

import sys
import processjob

if len(sys.argv) != 2:
    print "The command to be run, and its options must be passed as a quoted string"
    sys.exit()

COMMANDSTRING = sys.argv[1]
sys.stderr.write("Commandstring as passed in: " + COMMANDSTRING + "\n")

OUTPUTLINES = processjob.parseCommandString(COMMANDSTRING)
print "\n".join(OUTPUTLINES)