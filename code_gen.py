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

usage="""Usage:
    code_gen.py filename  -> return generated code to stdout
    code_gen.py -i filename -> change code in place
    code_gen.py -d filename -> open meld to see difference between exiting and generarated code
"""

def check_file(filename):
    if not os.path.isfile(filename):
        print(usage)
        raise ValueError(f"Error: {filename} does not exist")
    return filename


if len(sys.argv)==1:
    print(usage)
    sys.exit(0)
elif len(sys.argv)==2:
    inplace="print"
    filename=sys.argv[1]
    check_file(filename)
elif len(sys.argv)==3:
    if sys.argv[1]=='-i':
        inplace="yes"
        filename=sys.argv[2]
        check_file(filename)
    elif sys.argv[1]=='-d':
        inplace="diff"
        check_file(filename)
    else:
       print(usage)
       sys.exit(0)

newfile=[]
cmd=[]
newfileapp=True
cmdapp=False
for line in open(filename):
    if line.startswith("/* code_gen python"):
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

