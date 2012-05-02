#!/usr/bin/Py

import tilemap

""" Avatar Module

Implements the plane which the user will write code
for, as well as the underlying airplane skeleton which
contains more advanced functionality.

Author: jwoberbe
Date: 4.23.12
"""

class CrashException(Exception):
    def  __init__(self, value="You've hit a wall or grue."):
        self.value = value;
    def __str__(self):
        return repr(self.value);

class VictoryException(Exception):
    def __init__(self, value="Level Completed"):
        self.value = value;
    def __str__(self):
        return repr(self.value);

class Airplane:
    """Airplane class

    This object is the underlying skeleton of the avatar
    which the user writes the level method for.
    Constructor takes in a reference to the map which the
    plane is contained in.
    """
    
    def __init__(self, tile_map):
        self.dummy = False
        self.heading = 0
        self.tileMap = tile_map
        self.moveSet = ""

    def setDummy(self, boolean):
        self.dummy = boolean;
        if boolean:
            self.resetMoves()

    def getMoves(self):
        """
        returns the moves that the plane makes during
        a level. 
        0=moveRight
        1=moveUp
        2=moveLeft
        3=moveDown
        4=turnLeft
        5=turnRight
        6=crash
        7=victory
        -1=ERROR
        """
        return self.moveSet;

    def resetMoves(self):
        self.moveSet = ""

    def setHeading(self, heading):
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
        if self.dummy:
            self.moveSet += "6"
            raise CrashException()

    def askName(self):
        """
        This method is used for binary search level
        """
        try:
            a = self.tileMap.askName()
            return a
        except VictoryException:
            self.moveSet += "7"
        except tilemap.OutOfGuessException:
            self.crash()

    def check(self):
        front = self.tileMap.check(self.heading)
        if front == "WALL" or front == "ISLAND":
            return "CLOUD"
        if front == "AIR":
            return "AIR"
        if front == "GATE":
            return "TARGET"

    def turnLeft(self):
        #TODO add in animation calls here
        self.heading = (self.heading+1)%4
        if self.dummy:
            self.moveSet += "5"

    def turnRight(self):
        self.heading = (self.heading-1)%4
        if self.dummy:
            self.moveSet += "4"

    def move(self):
        try:
            if self.dummy:
                self.moveSet += str(self.heading)
            self.tileMap.move(self.heading)
        except VictoryException:
            self.moveSet += "7"
        except tilemap.InvalidMoveException:
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
