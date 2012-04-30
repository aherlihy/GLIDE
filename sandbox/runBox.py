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
#        print compiler_output
        list = compiler_output.split(':', 1)
#        print list
        
        if(list[0]=="Sorry"):
            list = list[1].split(':', 1)
            output.write(list[0].strip())
        else:
            output.write(list[0].strip())
        list = list[len(list)-1]#This will be the lefthand side of the error message, after <errortype>:
        list = list.split('\'',5)
        output.write(": " + list[1]+"\n")#write the subtype of error
#        print list
        nums = list[4].split(',')
        output.write("line " + nums[1].split()[0]+"\n")#row
        #output.write("col(should this be included?): " + nums[2].split()[0]+"\n")#col
        output.write("code: \"" +list[5][4:-4]+"\"\n")
#        output.write(compiler_output)#full output
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
#    print("printing stderr " + run_output)
#    for i in run_output:
#        print i
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

#           print len(list)
           length = len(list)
           codeline = "None"
           currentErrorFile = "None"
           linenumber = "None"
           reasonableError = False
           for i in range (0,length):
               if(list[i].startswith("  File")):
                   #print "line starts with File", list[i]
                   fileline = list[i].split(',')
                   linenumber = fileline[1].strip()
                   codeline = list[i+1]
                   filename = fileline[0].split('\"')
                   #print filename
                   for name in filename:
                       if(name.endswith(".py")):
                           currentErrorFile = name
                   if(currentErrorFile.endswith("runLevel.py")):
                       reasonableError=True
                       break
#           print "linenumber: ", linenumber, " codeline: \"", codeline, "\" currentErrorFile: ", currentErrorFile
           if not(reasonableError):
               output.write("Oh no, looks like there was an error that didn't originate in the user's code. It came from " + currentErrorFile + "\n")
           output.write(list[length-1]+"\n")
           output.write(linenumber + "\n")
#           print "len-1", codeline[len(codeline)-1]
#           print "len-2", codeline[len(codeline)-2]
           output.write("code: \"" + codeline[4:] + "\"")
#           output.write("\nFULL: \n" + run_output)
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
        output.write("Hey! Great job, it looks like your code is correct. Problem is, it's trying to do something that's not allowed.\n\n")
        list = r.split('\n')
        for line in list:
            if(line==""):
                break
            a = line.split('|')
            output.write("The module you used was " + a[0] + "\n")
            b = a[1].split(':')
            output.write("line " + b[1] + "\n")
            for i in range(2, len(a)):
                c=a[i].split(':')
                if(c[0]=="FROM"):
                    output.write("(You never need to import outside packages! We've taken care of everything you're going to need)\n\n")
                    #don't do anything with the name of the imported functions - not really important so not printed. Basically, as soon as the line has been identified there's no question that they shouldn't be importing it    
        output.close()
        file.close()
        return False
def run(map_path):
    output = open("output.py", "w")
    box = sandbox() 
    if not(box.init_level()):
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

#print("compiling...")
#try:
#    py_compile.compile(sys.argv[1], doraise=True)
#except py_compile.PyCompileError, e:
#    print ("CERROR:", e)
#else:
#    print("no errors :/")
if __name__ == '__main__':
    run("../support/levels/level3")
