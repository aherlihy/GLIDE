#!/usr/bin/Python

from tilemap import *
from avatar import *

if __name__ == '__main__':
    print "!"
    a = TileMap("map1")
    plane = a.getPlane()
    a.runLevelDummy()
    print "commands are: " + a.runLevel()
