#! /usr/bin/env python

import sys
import processjob
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("commandline", nargs="+")
# TODO - can only handle one external group at presnt. Unclear why
# argparse should allow > 1 arguments with the same name
parser.add_argument("--extvar",  nargs="+")
args = parser.parse_args()

if len(args.commandline) != 1:
    print "The command to be run, and its options must be passed as a quoted string"
    sys.exit()

COMMANDSTRING = args.commandline[0]
sys.stderr.write("Commandstring as passed in: " + COMMANDSTRING + "\n")

OUTPUTLINES = processjob.parseCommandString(COMMANDSTRING, args.extvar)
print "\n".join(OUTPUTLINES)