#! /usr/bin/env python

"""  Job builder - build a script for the jobrunner script.  
Given information on the experiment part, and the tracking source(s) we wish to use it will
construct a jobrunner script to (repeatedly) execute abc-classify with the appropriate parameters
"""

import argparse
import pandas as pd
import sys

def getJobName(sources):
    """ Generate the job name.
    This is the sorted and concatenated list of tracker sources"""

    jobname = '_'.join(sorted(sources))

    return jobname

def generateTrackingFlags(sources):
    """ Given a pandas dataframe of the required tracker sources, generate a list
    containing the appropriate data for the jobrunner's --trackerfile parameter"""

    sourcelocs = sources.Location.astype(str).str.cat(sources.Filename.astype(str), sep="/").tolist()

    return sourcelocs

parser = argparse.ArgumentParser(description = "Build a jobrunner script")
parser.add_argument("--sources", nargs="*")
parser.add_argument("--lookup", type = str, help="The lookup table of tracking source names and locations", required=True)
parser.add_argument("--print", action="store_true", required=False )
parser.add_argument("--debug", required=False, action="store_true")
parser.add_argument('--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
parser.add_argument("--resultsdir", type = str, default="/idinteraction/output/",
    help = "The root directory for the results.  The results for this specific job will be in [resultdir]/jobname")
parser.add_argument("--commandname", type = str, default="/idinteraction/abc-display-tool/abc-classify.py",
    help = "The command to run in the job script")

args, unknownargs = parser.parse_known_args()

# TODO - put this in a function and check we have appropriate columns
lookupData = pd.read_csv(args.lookup)
jobname = getJobName(args.sources)

if args.debug:
    print lookupData

    print args
    print "***"
    print unknownargs
    print jobname

wantedSources = lookupData[lookupData["NiceName"].isin(args.sources)]

if len(wantedSources) != len(args.sources):
    raise ValueError("Could not find all requested sources")

trackingFlags = generateTrackingFlags(wantedSources)
outdir = args.resultsdir + jobname

outfile = args.outfile

outfile.write(outdir + "\n")
outfile.write(args.commandname)
outfile.write(" ")
outfile.write(" ".join(unknownargs))
outfile.write(''.join([" --trackerfile " + s for s in trackingFlags]))
outfile.write("\n")

