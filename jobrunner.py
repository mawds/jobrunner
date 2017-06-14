#! /usr/bin/env python

import sys
import processjob
from argparse import ArgumentParser
import re

parser = ArgumentParser()
parser.add_argument("commandline", nargs="+")
parser.add_argument("--extvar",  nargs="+", action="append")
parser.add_argument("--extvarfile", nargs="+", action="append")
args = parser.parse_args()

if len(args.commandline) != 1:
    print "The command to be run, and its options must be passed as a quoted string"
    sys.exit()

COMMANDSTRING = args.commandline[0]
sys.stderr.write("Commandstring as passed in: " + COMMANDSTRING + "\n")

if bool(args.extvar is not None) & bool(args.extvarfile is not None):
    print "Can only specify external variables on command line OR in a file"
    sys.exit()


extvar = [] 
if args.extvarfile is not None:
    for evf in args.extvarfile:
        m = re.search(r"^(\w):(.*)", evf[0])
        if m:
            groupname = m.group(1)
            filename = m.group(2)
            with open(filename,"r") as f:
                pars = f.readline().strip()
            extvarstring =  groupname + ":" + pars
            extvar.append([extvarstring])
        else:
            print "Cannot parse extvarfile"
            sys.exit()

if args.extvar is not None:
    extvar = args.extvar

OUTPUTLINES = processjob.parseCommandString(COMMANDSTRING, extvar)
print "\n".join(OUTPUTLINES)