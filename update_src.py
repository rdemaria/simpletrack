#!/usr/bin/env python3

import os,sys

import subprocess
def exe(input):
    return subprocess.run('python3', input=input,
                   stdout=subprocess.PIPE,
                   universal_newlines=True).stdout

if sys.argv[1]=='-i':
    inplace=True
    filename=sys.argv[2]
else:
    inplace=False
    filename=sys.argv[1]
    if not os.path.isfile(filename):
        raise ValueError(f"{filename} does not exist")

newfile=[]
cmd=[]
newfileapp=True
cmdapp=False
for line in open(filename):
    if line.startswith("/* python"):
        cmd=[]
        cmdapp=True
    elif line.startswith("/* end python"):
        newfileapp=True
        newfile.append(exe(''.join(cmd)))
    elif cmdapp==True:
        if line.startswith("*/"):
            cmdapp=False
            newfile.append(line)
            newfileapp=False
        else:
            cmd.append(line)
    if newfileapp:
        newfile.append(line)

newfile=''.join(newfile)
if inplace:
    open(filename,'w').write(newfile)
else:
    print(newfile)
