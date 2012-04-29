#!usr/bin/python
from tilemap import *
from avatar import *

def runLevel(plane):
    plane.turnLeft()
    plane.move()
    plane.turnRight()
    for i in range(9):
        plane.move()
    plane.turnLeft()
    plane.move()
