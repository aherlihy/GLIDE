#!usr/bin/python
from tilemap import *
from avatar import *

def runLevel(plane):
    plane.move()
    plane.move()
    plane.turnLeft()
    plane.turnRight()
    plane.turnLeft()
    f = open("output.py", "r")
    import sys
    sys.showprofile()
    return
