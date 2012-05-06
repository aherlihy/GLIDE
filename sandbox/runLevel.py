#!usr/bin/python
from tilemap import *
from avatar import *

def runLevel(plane):
    def explore(room):
        plane.markRoom()
        for n in plane.roomNeighbors(room):
            if not(plane.isMarked):
                plane.goto(n)
                explore(n)
                plane.goto(room)
    
    start = plane.whereAmI()
    explore(start)
    
    

    return
