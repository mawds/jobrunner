#!/usr/bin/python

"""Script to read in some arguments and dump to file.  Used to test jobrunner"""


import argparse
import sys

parser = argparse.ArgumentParser(description = "Testfile")

parser.add_argument("--outputfile", type=str, required=True)
parser.add_argument("--input1", type=float, required=True)
parser.add_argument("--input2", type=float, required=True)


args=parser.parse_args()

with open(args.outputfile, "a") as f:
    f.write(str(args.input1) + "," + str(args.input2) + "," + str(args.input1*args.input2) + "\n")