#! /usr/bin/env python

import sys
import processjob
from argparse import ArgumentParser
import re

parser = ArgumentParser()
parser.add_argument("commandline", nargs="+")
# TODO - can only handle one external group at presnt. Unclear why
# argparse should allow > 1 arguments with the same name
# This is tested for below
parser.add_argument("--extvar",  nargs="+")
parser.add_argument("--extvarfile", nargs="+")
args = parser.parse_args()

if len(args.commandline) != 1:
    print "The command to be run, and its options must be passed as a quoted string"
    sys.exit()

COMMANDSTRING = args.commandline[0]
sys.stderr.write("Commandstring as passed in: " + COMMANDSTRING + "\n")

if not((args.extvar is None) ^ (args.extvarfile is None)):
    print "Can only specify external variables on command line OR in a file"
    sys.exit()


extvar = None
if args.extvarfile is not None:
    if len(args.extvarfile) > 1: 
        print "Don't currently handle > 1 extvar"
        sys.exit()
    m = re.search(r"^(\w):(.*)", args.extvarfile[0])
    if m:
        groupname = m.group(1)
        filename = m.group(2)
        with open(filename,"r") as f:
            pars = f.readline().strip()
        extvarstring =  groupname + ":" + pars
        extvar = [extvarstring]
    else:
        print "Cannot parse extvarfile"
        sys.exit()

if args.extvar is not None:
    if len(args.extvar) > 1: 
        print "Don't currently handle > 1 extvar"
        sys.exit()
    extvar = args.extvar

OUTPUTLINES = processjob.parseCommandString(COMMANDSTRING, extvar)
print "\n".join(OUTPUTLINES)