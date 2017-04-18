# Jobrunner

This program is used to sweep through a series of parameters when calling a program.  For example

`jobrunner.py "myprog -size {20,40} -age {30,50,55}"`

Will print the following, which can be put in a script etc.: 

```
myprog -size 20 -age 30
myprog -size 20 -age 50
myprog -size 20 -age 55
myprog -size 40 -age 30
myprog -size 40 -age 50
myprog -size 40 -age 55
```

Note that we pass the command line as a quoted string to prevent interferance by the shell. It's `myprog`'s responsibilty to do something sensible with the output files.  The ordering of the output command lines is arbitrary.

An additional syntax element is also supported.  If multiple files need to be loaded relating to the same experimental unit, then we can do stem expansion:

```
jobrunner.py "myprog -auxfile {p: P01, P02}_auxfile.csv -datafile data{p:}.txt -size {20,40}"
```

will run generate:

```
myprog -auxfile P01_auxfile.csv -datafile dataP01.txt -size 20
myprog -auxfile P02_auxfile.csv -datafile dataP02.txt -size 20
myprog -auxfile P01_auxfile.csv -datafile dataP01.txt -size 40
myprog -auxfile P02_auxfile.csv -datafile dataP02.txt -size 40
```







