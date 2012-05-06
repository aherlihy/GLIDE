#!usr/bin/python
from tilemap import *
from avatar import *

def runLevel(plane):
    
    a = plane.whereAmI()
    b = plane.roomNeighbors(a)
    plane.goto(b[0])

    return
