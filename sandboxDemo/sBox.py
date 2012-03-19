#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

# This file represents the sandbox that will be generated for the user's code
# For now, the command-line args will contain the pathfile to the process to be run inside this process
# This code snippet will be included in the main process, and instead of being passed a command-line arg, the process will be generated from the user input

# Once the process is started, it will execute and exit, passing the exit information to the sandbox
# NOTE - the goal of this sandbox is not to figure out what the process does. The goal is to run to process and catch any runtime or compile-time errors.

import sys
import subprocess
import py_compile

#define a function that will take in a variable number of arguments and ret$
def cmd_output(args, **kwds):
    kwds.setdefault("stdout", subprocess.PIPE)
    kwds.setdefault("stderr", subprocess.STDOUT)
    p = subprocess.Popen(args, **kwds)
    return p.communicate()[0]

print("helloo")

#compile the code and check for any syntax errors
try:
    py_compile.compile(sys.argv[1], doraise=True)
except py_compile.PyCompileError, e:
    print "Oops! Looks like there's a compiler error:"
    print "\t",e
#if there are no compile-time errors, run the code and check for any runtim$
else:
    print "Oops! Looks like there's a runtime error:"
    print cmd_output(["python", sys.argv[1]])
