#!/usr/bin/env python3

import os,sys,tempfile

import subprocess
def exe(input):
    sub=subprocess.run('python3', input=input,
                   stdout=subprocess.PIPE,
                   universal_newlines=True)
    if sub.returncode>0:
        print("Attempting running code:")
        print(cmd)
        print("Output:")
        print(sub.stdout)
        raise ValueError("Code generation failed")
    return sub.stdout

if sys.argv[1]=='-i':
    inplace="yes"
    filename=sys.argv[2]
elif sys.argv[1]=='-d':
    inplace="diff"
    filename=sys.argv[2]
else:
    inplace="print"
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
        if len(cmd)>0:
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
if inplace=="yes":
    open(filename,'w').write(newfile)
elif inplace=="print":
    print(newfile)
elif inplace=="diff":
    tfile,tfilename=tempfile.mkstemp()
    open(tfile,'w').write(newfile)
    os.system(f"meld {filename} {tfilename}")
    os.unlink(tfilename)

