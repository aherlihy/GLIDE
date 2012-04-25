#!/usr/bin/python

from sBox import *

box = sandbox()
box.init_level()
print "compiler says: " + box.compile_usr()
print "process says: " + box.run_process(["python", "bubblewrap.py", "map1"])

print("finished run!")
