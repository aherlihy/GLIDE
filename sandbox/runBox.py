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
        output.write("Oh no! Looks like you've got an error in your code :(\nCheck out the help pages if you're not sure how to fix it!\n\n")
        output.write("COMPILER ERROR\n")
        #parse py_compiler exception
        list = compiler_output.split(':', 1)      
        if(list[0]=="Sorry"):#because the python compiler is inconsistently polite
            list = list[1].split(':', 1)
            output.write(list[0].strip())
        else:
            output.write(list[0].strip())
        list = list[len(list)-1]#This will be the lefthand side of the error message, after <errortype>:
        list = list.split('\'',5)
        output.write(": " + list[1]+"\n")#write the subtype of error
        nums = list[4].split(',')
        output.write("line " + nums[1].split()[0]+"\n")#row
        output.write("code: \"" +list[5][4:-4]+"\"\n")
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
def run_this(box, output, map_path):
    run_output = box.run_process(["python", "bubblewrap.py", map_path])
    if(run_output == "ERROR:TIMEOUT"):
        output.write("Yikes! Your code took too long to run :(\nYou probably have an infinite loop or you're doing something extremely inefficiently\nCheck out the help pages if you're not sure how to fix it!\n\n")
        output.write("RUNTIME ERROR\n")
        output.write("Timeout\n")
        output.close()
        return False
    else:
        if(run_output == "" or run_output==None):
           output.write("NO ERRORS!\n")
           output.write("Careful though - your code may be correct but not do exactly what you want\n")
           output.close()
           return True
        else:
           errorfile = open("errorfile", "w")
           errorfile.write(run_output)
           errorfile.close()
           list = run_output.strip().split('\n')
           output.write("Oh no! Looks like you've got an error in your code :(\nCheck out the help pages if you're not sure how to fix it!\n\n")           
           output.write("RUNTIME ERROR\n")

           length = len(list)
           codeline = "None"
           currentErrorFile = "None"
           linenumber = "None"
           reasonableError = False
           for i in range (0,length):
               if(list[i].startswith("  File")):
                   fileline = list[i].split(',')
                   linenumber = fileline[1].strip()
                   codeline = list[i+1]
                   filename = fileline[0].split('\"')
                   for name in filename:
                       if(name.endswith(".py")):
                           currentErrorFile = name
                   if(currentErrorFile.endswith("runLevel.py")):
                       reasonableError=True
                       break
           if not(reasonableError):
               output.write("Oh no, looks like there was an error that didn't originate in the user's code. It came from " + currentErrorFile + "\nYou can check out errorfile for the full stack trace\n")
           output.write(list[length-1]+"\n")
           output.write(linenumber + "\n")
           output.write("code: \"" + codeline[4:] + "\"")
           output.close()
           return False
def analyze_ast(box, output):
    box.gen_AST()
    file = open("astoutput", "r")
    r = file.read()

    if(r == ""):
        file.close()
        return True
    else:
#        output.write("Hey! Great job, it looks like your code is correct. Problem is, it's trying to do something that's not allowed.\n\n")
        list = r.split('\n')
        noErrors=True
        for line in list:
             if(line.startswith("|")):
                 continue
             elif(line.startswith("Import")):
                 noErrors=False
                 breaks=line.split('|')
                 output.write("The module you used was " + breaks[0] + " on line " + breaks[1].split(':')[1] + "\n")
                 output.write("(You never need to import outside packages! We've taken care of everything you're going to need)\n\n")
             elif(line.startswith("Call")):
                 breaks=line.split('|')
                 if(("NAME:plane" in line) or ("NAME:range" in line) or ("NAME:len" in line) or ("NAME:n" in line) or ("NAME:room" in line) or ("NAME:explore" in line)):
                     continue
                 else:
                     noErrors=False
                     output.write("It looks like you're trying to call a function that's not allowed.\n")
                     for b in breaks[1:]:
                          print "b", b
                          c = b.split(':')
                          if(c[0]=="LINE"):
                               output.write("On line " + c[1]+ " you call ")
                          if(c[0]=="ATTRIBUTE"):
                               output.write("\"" + c[1] + "\"")
                          if(c[0]=="NAME"):
                               output.write(" on \"" + c[1] + "\"")
                     output.write("\n\n")
        file.close()
        if(noErrors):
            return True
        else:
            output.close()
            return False
# Top-level method call. This will be called by the support code.
# This sandbox is able to take different code without reinitializing everything, but unfortunately the support code needs to be re-initialized each time, and the sandbox is contained in that code, so this will be reinited each time.
def run(map_path, level, user):
    output = open("output.py", "w")
    box = sandbox() 
    if not(box.init_level(level, user)):
        output.write("ERROR:EMPTY")
        output.close()
        return False
    if not(compile_this(box, output)):
	return False
    if not (analyze_ast(box, output)):
        return False
    if not(run_this(box, output, map_path)):
        return False
    return True
if __name__ == '__main__':
    run("../support/levels/level6", 6, "anna")
