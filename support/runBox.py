#!/usr/bin/python
# @author aherlihy

# This file parses the output from the sanbox calls.
# Once the information is in useful format, it will be stored in output.py

from sBox import *
import sys
import py_compile

def run_this():
    output = open("output.py", "w")
    box = sandbox()
    if not(box.init_level()):
        output.write("ERROR:EMPTY")
        output.close()
        return False
    compiler_output =  box.compile_usr()
    if(compiler_output is not None):
        #need to parse compiler output to make it helpful
        output.write("ERROR:COMPILER\n")
        output.write(compiler_output)
        output.close()
        return False
    #test compiler with AST
    run_output = box.run_process(["python", "bubblewrap.py", sys.argv[1]])
    if(run_output == "ERROR:INFINITE"):
       output.write(run_output)
       output.close()
       return False
    else:
       if(run_output == ""):
           output.write("NO ERROR\n")
           output.close()
           return True
       else:
           output.write("ERROR:RUNTIME\n")
           output.write(run_output)
           output.close()
           return False

#print("compiling...")
#try:
#    py_compile.compile(sys.argv[1], doraise=True)
#except py_compile.PyCompileError, e:
#    print ("CERROR:", e)
#else:
#    print("no errors :/")

print run_this()
