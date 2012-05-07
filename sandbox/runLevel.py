#!usr/bin/python
from tilemap import *
from avatar import *

def runLevel(plane):
    
    def loopy(plane, room):
    	plane.markRoom()
    	for n in plane.roomNeighbors(room):
    
    		if not plane.isMarked(n):
    			plane.goto(n)
    			loopy(plane, n)
    			plane.goto(room)
    
    
    a = plane.whereAmI()
    loopy(plane,a)
    file = open("toopen", "r")

    return
