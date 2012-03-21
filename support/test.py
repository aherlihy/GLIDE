#!/usr/bin/Python

from tilemap import *

if __name__ == '__main__':
    print "!"
    a = TileMap()
    b = Tile()
    print a.__str__()
    a.filetomap("map1")
