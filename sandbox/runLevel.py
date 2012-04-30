#!usr/bin/python
from tilemap import *
from avatar import *

def runLevel(plane):
    file = open("errorfile", 'w')
    print "this"
    print "this", file
    
    plane.move()
    plane.check()
    plane.move()
    
    
    return
