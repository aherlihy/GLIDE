#! /usr/bin/python

# This is the bubblewrapped environment for the user input
# It takes in the level map as to know which enviornment to mimic
# The user's code will be appended to the function run_level(...)
# Here, the user script will be manipulating a dummy plane and map. 
# If the script passes the tests then the function runLevel will be passed over to the support classes
# The support class will take the script and run it on the actual vars.

# @author aherlihy

# MAIN:	

from tilemap import *
from avatar import *
from runLevel import *
import sys

#set up dummy variables
mapArg = sys.argv[1]
map = TileMap()
map.filetomap(mapArg)
plane = map.getPlane()
runLevel(plane, map)

