#!/usr/bin/Python

from tilemap import *
from avatar import *

if __name__ == '__main__':
    print "!"
    a = TileMap()
    print a
    a.filetomap("map1")
    plane = Airplane(a)
    a.setPlane()
    plane.move()
    print a
    plane.move()
    print a
    plane.move()
    print a
    plane.move()
    print a
    plane.move()
    print a
    plane.turnLeft()
    print a
    plane.move()
    print a
