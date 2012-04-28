#!/usr/bin/Py

from tilemap import *

""" Avatar Module

Implements the plane which the user will write code
for, as well as the underlying airplane skeleton which
contains more advanced functionality.

Author: jwoberbe
Date: 4.23.12
"""

class Airplane:
    """Airplane class

    This object is the underlying skeleton of the avatar
    which the user writes the level method for.
    Constructor takes in a reference to the map which the
    plane is contained in.
    """
    
    def __init__(self, tile_map):
        self.heading = 0
        self.tileMap = tile_map
        self.tileMap.setPlane()

    def setHeading(heading):
        """
        heading refers to which direction the plane is
        facing.
        0=right
        1=up
        2=left
        3=down
        """
        self.heading = heading%4

    def crash(self):
        """
        This method will be called whenever the plane
        runs into an immmovable object (NPC, wall, fire,
        etc.)
        """
#        print "CRASH!!!"
        #TODO

    def check(self):
        return self.tileMap.check(self.heading)

    def turnLeft(self):
        #TODO add in animation calls here
        self.heading = (self.heading+1)%4

    def turnRight(self):
        self.heading = (self.heading-1)%4

    def move(self):
        try:
            self.tileMap.move(self.heading)
        except InvalidMoveException:
            self.crash()



class Plane(Airplane):
    """Plane class

    This is the wrapper which the user will use to control
    the plane.  It has minimal functionality to prevent
    confusion or cheating.
    The purpose of encapsulation is to remove instance
    variables from this class, as well as unwanted
    functionality.
    """

    def __init__(self, tile_map):
        #sadly, I see no way to get around a parameter
        super(Plane, self).__init__(tile_map)


    def move(self):
        Airplane.move(self)

    def check(self):
        Airplane.check(self)

    def turnLeft(self):
        Airplane.turnLeft(self)

    def turnRight(self):
        Airplane.turnRight(self)
