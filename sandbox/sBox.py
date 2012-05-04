#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

# @author aherlihy
# This file represents the sandbox that will be generated for the user's code
# The constructor args will be:
    # (1) the level number
    # (2) the username
# It's assumed that the main process has saved the users code in a plaintext file named "code<level><username>"

# The content of code<...> will be appended to the end of the runLevel.py file so it can be imported by bubblewrap.py

# bubblewrap.py is the dummy environment that this sandbox will run

# Once the process is started, it will execute and exit, passing the exit information to the sandbox
# NOTE - there are 3 different goals of this sandbox.
     #The first is to catch any compile-time errors and produce useful error messages
     #The second is to catch any runtime errors (including infinite loops, which are done with a timeout)
     #The third is to figure out what the users code is trying to do and to check to see if there is anything dangerous going on.

# Due to the nature of the user code being tested, it was decided that using pexpect or a different thread was overkill. 
# The user scripts are not interactive and should not be doing anything above the functionality of a DFS. There's no need to control the IO except to pipe stderr and throw away stdout. 

# Imports and other dangerous functionality are stripped by generating an abstract syntax tree using the built-in compiler module for python. A visitor is then defined to 
# explore the AST and if anything is found that shouldn't exist, the process will exit. 

# The AST will also be used to try and ease the transition to compiler errors. For example, if a whitespace error occurs we can produce much more helpful output than the compiler can.

# Once the user script passes compiling and the specialized AST analysis, the program is presumed safe to run and will be passed back to the game engine.

import sys
import subprocess
import py_compile
import time
import ast
from ASTvisitor import *

#This is the sandbox class
class sandbox:

    # init doesn't really need to do anything because there are no global vars
    def __init__(self):
        pass

    # initializes the level file by appending the user's script to a function definition with the correct imports
    # saves the file as runLevel<#>
    def init_level(self, level, user):
        #set up headers
        outfile = open("runLevel.py", "w")
        outfile.write("#!usr/bin/python\n")
        outfile.write("from tilemap import *\n")
        outfile.write("from avatar import *\n\n")
        outfile.write("def runLevel(plane):\n")
        code = "code" + str(level) + user
        codefile = open(code, "r")
        empty = True

        #append each line in codefile to outfile, indenting appropriately
        for line in codefile:
            empty = False
            outfile.write("    ")
            outfile.write(line)
        outfile.write("\n    return\n")
        if(empty):
            return False
        codefile.close()
        outfile.close()
        return True
      
    # compile will check runLevel through the compiler and catch any syntax errors
    def compile_usr(self):
        #compile the code and check for any syntax errors
        try:
            py_compile.compile("runLevel.py", doraise=True)
        except py_compile.PyCompileError, e:
            return (e.__str__())
        else:
            return (None)

    # takes in a variable number of arguments and return the output of the process being run.
         # limits the period that the subprocess will run to a few seconds. Any code that takes longer than that is either in an infinite loop or is doing something rediculously slow.
    def run_process(self, args, **kwds):
        file = open("justforfunsiez", "w")#exists in case we introduce printlines to our program.
        file.write("This file is where the stdout of the subprocess will go. For debugging")
        kwds.setdefault("stdout", file)#pipe stdout to a file
        kwds.setdefault("stderr", subprocess.PIPE)#pipe stderr to the output of the subprocess
        usr = subprocess.Popen(args, **kwds)
        time.sleep(3)
        if(usr.poll() == None):
            usr.kill()
            file.close()
            return ("ERROR:TIMEOUT")
        else:
            toreturn =  usr.communicate()[1]
            file.close()
            return toreturn
    # generate the AST and parse for illegal imports or obvious errors
    # if there's time, pass a flag into the request and look for different specific issues depending on the level
    def gen_AST(self):
        
        visitor = ASTvisitor()
        file = open("runLevel.py", "r")
        ASTfile = open("astoutput", "w")
        printfile = open("tsa", "w")
        printfile.close()
        ASTfile.close()
        usrcode = file.read()
        tree = ast.parse(usrcode)
        visitor.generic_visit(tree)
