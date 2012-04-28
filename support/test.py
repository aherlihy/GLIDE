#!/usr/bin/Python

from tilemap import *
from avatar import *

if __name__ == '__main__':
    print "!"
    a = TileMap("map1")
    plane = a.getPlane()
    print a
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
