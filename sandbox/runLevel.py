#!usr/bin/python
from tilemap import *
from avatar import *

def runLevel(plane):
<<<<<<< HEAD
    import sys
    sys.showprofile()
    file = open("output.py", "r")
=======
    plane.move()
    plane.move()
    plane.turnLeft()
    plane.turnRight()
    plane.turnLeft()
    f = open("output.py", "r")
    import sys
    sys.showprofile()
>>>>>>> 7ad0f2b6fcd5abc88b619e7765b41bc300446af4
    return
