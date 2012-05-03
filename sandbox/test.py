#!/usr/bin/Python

from tilemap import *
from avatar import *

if __name__ == '__main__':
    print "!"
    a = TileMap("../support/levels/level3")
    plane = a.getPlane()
    plane.move()
    plane.check()
    print "commands are: " + a.getLevel()
