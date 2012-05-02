#!usr/bin/python
from tilemap import *
from avatar import *

def runLevel(plane):
    for i in range(0,3):
        plane.move()
    plane.turnLeft()
    plane.move()
    plane.turnRight()
    for i in range(0,6):
        plane.move()
    plane.turnLeft()
    plane.move()
    return
