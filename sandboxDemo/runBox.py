#!/usr/bin/python
# @author aherlihy

# This file parses the output from the sanbox calls.
# Once the information is in useful format, it will be stored in output.py

from sBox import *
import sys
import py_compile

# compiles the code and parses any errors into the format:
    # ERROR:COMPILER
    # <ErrorType>
    # <SubType>
    # <line>
    # <col>
    # unparsed compiler output
def compile_this(box, output):
    compiler_output =  box.compile_usr()
    if(compiler_output is not None):
        output.write("ERROR:COMPILER\n")
        #parse py_compiler exception
        list = compiler_output.split(':', 2)
        if(len(list)==2):
            output.write(list[0].strip() + "\n")#write the type of error
        else:
            output.write(list[1].strip() + "\n")
        list = list[len(list)-1]
        list = list.split('\'',5)
        output.write(list[1]+"\n")#write the subtype of error
        nums = list[4].split(',')
        output.write(nums[1].split()[0]+"\n")#row
        output.write(nums[2].split()[0]+"\n")#col
        output.write(list[5][:-3]+"\n")
        output.write(compiler_output)#full output
        output.close()
        return False
    else:
	return True
# Runs the code and parses any errors thrown
# Could dynamically parse the traceback and build an awesome flowchart of what's calling what
# Only thing is that the user only ever writes one method. Maybe if this program is extended to huge levels, but for now that's overkill and we can ignore the traceback entirely.
# The format that this method produces if a runtime error is caught is:
     # ERROR:RUNTIME
     # <line-number> (in the users code, even if the error is thrown elsewhere)
     # <line> (users code)
     # <Error name + description>
def run_this(box, output):
    run_output = box.run_process(["python", "bubblewrap.py", sys.argv[1]])
    if(run_output == "ERROR:TIMEOUT"):
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
           list = run_output.strip().split('\n')
           
           print len(list)
           length = len(list)
           for i in range (0,length):
               if(list[i].startswith("  File \"/gpfs/main/home/aherlihy/GLIDE/support/runLevel.py\",")):
                   line = list[i].split(',')
                   output.write(line[1].strip() + "\n")
                   output.write(list[i+1].strip() + "\n")
           output.write(list[length-1]+"\n")
           output.write("\nFULL: \n" + run_output)
           output.close()
           return False
def test():
    output = open("output.py", "w")
    box = sandbox() 
    if not(box.init_level()):
        output.write("ERROR:EMPTY")
        output.close()
        return False
    if not(compile_this(box, output)):
	return False
    #test compiler with AST
    if not(run_this(box, output)):
        return False
    box.gen_AST()
    return True

#print("compiling...")
#try:
#    py_compile.compile(sys.argv[1], doraise=True)
#except py_compile.PyCompileError, e:
#    print ("CERROR:", e)
#else:
#    print("no errors :/")

box = sandbox()

box.init_level()

box.gen_AST(sys.argv[2])
