#!usr/bin/python
from tilemap import *
from avatar import *

def runLevel(plane):
    a = plane.whereAmI()
    b = plane.roomNeighbors(a)
    print "!"
    print b
    print "?"
    print b[0]
    print "@"
    plane.goto(b[0])
    list = []
    print len(list)

    return
