#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

# This file represents the sandbox that will be generated for the user's code
# For now, the command-line args will contain the pathfile to the process to be run inside this process
# This code snippet will be included in the main process, and instead of being passed a command-line arg, the process will be generated from the user input

# Once the process is started, it will execute and exit, passing the exit information to the sandbox
# NOTE - the goal of this sandbox is not to figure out what the process does. The goal is to run to process and catch any runtime or compile-time errors.
# Due to the nature of the processes being tested, it was decided that using pexpect or a different thread was overkill. 
# The user scripts are not interactive and should not be doing anything above the functionality of a DFS. There's no need to control the IO except to pipe it to a file. 

# Imports and other dangerous functionality are stripped by generating an abstract syntax tree using the built-in compiler module for python. A visitor is then defined to 
# explore the AST and if anything is found that shouldn't exist, the process will exit. 

# The AST will also be used to try and ease the transition to compiler errors. For example, if a whitespace error occurs we can produce much more helpful output than the compiler can.

# Once the user script passes compiling and our specialized AST analysis, the program is presumed safe to run and will be passed back to the game engine.

import sys
import subprocess
import py_compile
import time
#define a function that will take in a variable number of arguments and return the output of the process being run.
#this function limits the period that the subprocess  will run to 10 seconds. Any code that takes longer than that is either in an infinite loop or is doing something rediculously slow.
def cmd_output(args, **kwds):
    kwds.setdefault("stdout", subprocess.PIPE)
    kwds.setdefault("stderr", subprocess.STDOUT)
    p = subprocess.Popen(args, **kwds)
    time.sleep(10) 
    if(p.poll() == None):
        p.kill() 
        return ("Either your code is stuck in an infinite loop or you've coded something much too slow!")
    else:
         return p.communicate()[0]
# START
print("Compiling code...")

#compile the code and check for any syntax errors
try:
    py_compile.compile(sys.argv[1], doraise=True)
except py_compile.PyCompileError, e:
    print "Oops! Looks like there's a compiler error:"
    print "\t",e
#if there are no compile-time errors, run the code and check for any runtime errors.
else:
    print "Great! No compiler errors. Running..."
    output =  cmd_output(["python", sys.argv[1]])
    print "Run completed. Program outputs: "
    print "---------------------"
    print output
    print "---------------------"
