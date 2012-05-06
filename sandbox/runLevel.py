#!usr/bin/python
from tilemap import *
from avatar import *

def runLevel(plane):
    room = plane.whereAmI()
    plane.roomNeighbors(room)
    
    

    return
