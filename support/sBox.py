#! /usr/bin/python
# -*- coding: iso-8859-1 -*-


# This file represents the sandbox that will be generated for the user's code
# For now, the command-line args will be:
    # (1) the level  number
    # (2) the pathfile to where the users input is saved
# It's assumed that the main process has saved the users code in a plaintext file named "code<#>"

# The content of code<#> will be appended to the end of the runLevel.py file so it can be imported by bubblewrap.py

# bubblewrap.py is the dummy environment that this sandbox will run

# Once the process is started, it will execute and exit, passing the exit information to the sandbox
# NOTE - the goal of this sandbox is not to figure out what the process does. The goal is to run to process and catch any runtime or compile-time errors, and strip any dangerous functionality.
# Due to the nature of the user code being tested, it was decided that using pexpect or a different thread was overkill. 
# The user scripts are not interactive and should not be doing anything above the functionality of a DFS. There's no need to control the IO except to pipe it to a file. 

# Imports and other dangerous functionality are stripped by generating an abstract syntax tree using the built-in compiler module for python. A visitor is then defined to 
# explore the AST and if anything is found that shouldn't exist, the process will exit. 

# The AST will also be used to try and ease the transition to compiler errors. For example, if a whitespace error occurs we can produce much more helpful output than the compiler can.

# Once the user script passes compiling and our specialized AST analysis, the program is presumed safe to run and will be passed back to the game engine.

import sys
import subprocess
import py_compile
import time

#This is the sandbox class
class sandbox:

    # TODO
    # init doesn't really need to do anything because there are no global vars
    def __init__():

    # TODO
    # initializes the level file by appending the user's script to a function definition with the correct imports
    # saves the file as runLevel<#>
    def init_level(levelNum):
        
    # compile will check runLevel through the compiler and catch any syntax errors
    def compile_usr(self):
        print("Compiling code...")
        #compile the code and check for any syntax errors
        try:
            py_compile.compile("bubblewrap.py", doraise=True)
        except py_compile.PyCompileError, e:
           return "Oops! Looks like there's a compiler error:" + e

    # takes in a variable number of arguments and return the output of the process being run.
         # limits the period that the subprocess  will run to 10 seconds. Any code that takes longer than that is either in an infinite loop or is doing something rediculously slow.
         # output =  run_process(["python", sys.argv[1]])
    def run_process(args, **kwds):
        kwds.setdefault("stdout", subprocess.PIPE)
        kwds.setdefault("stderr", subprocess.STDOUT)
        usr = subprocess.Popen(args, **kwds)
        time.sleep(10)
        if(usr.poll() == None):
            usr.kill()
            return ("Either your code is stuck in an infinite loop or you've coded something much too slow!")
        else:
             return usr.communicate()[0]
        
    # TODO
        # generate the AST and parse for illegal imports or obvious errors
        # if there's time, pass a flag into the request and look for different specific issues depending on the level
    def gen_AST():