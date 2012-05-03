#!/usr/bin/Python
import sys
sys.path.append('/home/ecacciat/GLIDE/sandbox');
import runBox
import random
from avatar import *

""" Map Module

Implements a basic map environment for use in GLIDE

Author: jwoberbe
Date: 3.19.12
"""

class MapBorderException(Exception):
    def __init__(self, value=""):
        self.value = value;
    def __str__(self):
        return repr(self.value);

class InvalidTileException(Exception):
    def __init__(self, value="Non-recognized Tile type attempted"):
        self.value = value;
    def __str__(self):
        return repr(self.value);
        
class InvalidMapFileException(Exception):
    def __init__(self, value="The Map format entered is in an invalid format."):
        self.value = value;
    def __str__(self):
        return repr(self.value);

class InvalidMoveException(Exception):
    def  __init__(self, value="You've hit a wall or grue."):
        self.value = value;
    def __str__(self):
        return repr(self.value);

class NoPlaneException(Exception):
    def __init__(self, value="There was no plane object on the given map."):
        self.value = value;
    def __str__(self):
        return repr(self.value);

class OutOfGuessException(Exception):
    def __init__(self, value="You're out of guesses!"):
        self.value = value;
    def __str__(self):
        return repr(self.value);


class Tile:
    """Map Tile Class

    This object represents a single tile of the map we will be displaying

    Author: jwoberbe
    Date:3.19.12
    """

    def __init__(self, value= "AIR") :
        self.valid = ["AIR","ISLAND","WALL","GATE","PLANE","DESK"]
        self.bitval = ["A","I","W","G","P","?"]
        self.value = "NULL"
        if value in self.valid:
            self.value = value
        else:
            for i in xrange(len(self.bitval)):
                if value == self.bitval[i]:
                    self.value = self.valid[i]
            if self.value == "NULL":
                raise InvalidTileException();
        

    def __str__(self):
        """ Returns a text representation of the tile in the
        map, for use of generating a text-based map of the
        level.
        """
        if self.value == "AIR":
            return "A";
        if self.value == "ISLAND":
            return "I";
        if self.value == "WALL":
            return "W";
        if self.value == "GATE":
            return "G";
        if self.value == "PLANE":
            return "P";
        if self.value == "DESK":
            return "?"

    def getType(self):
        return self.value;

    def setType(self, string):
        if string in valid:
            self.value = string
        else:
            raise InvalidTileException();

class TileMap:
    """Map Class

    This is the framework for the map we will display on the canvas.  It
    contains a tile for each "pixel" viewable, and will handle boundary
    checking, and the mutation of tiles as the plane interacts with them.

    grid is row-major order

    Author: jwoberbe
    Date:3.19.12
    """

    def __init__(self, map_path):
        #fix init to a set size, and edge in with clouds
        self.level = int(map_path[len(map_path)-1:])
        self.dummy = False
        self.map_path = map_path
        self.filetomap(map_path)
        if self.level == 5:
            pass;
            #TODO randomized Binary search stuff
        elif self.level == 6:
            pass;
            #TODO drunken walk stuff
        #sets the plane
        found = False
        self.plane = Airplane(self)
        for y in xrange(self.height):
            for x in xrange(self.width):
                if(self.grid[y][x].getType()=="PLANE"):
                    found = True
                    self.py = y
                    self.px = x
        if found == False:
            raise NoPlaneException() #there wasn't a plane 
    
    def createMaze(self):
        pass;
        #TODO Anna, I need your help here


    def initBinary(self):
        #TODO for the potential boxes in the maze, create random names
        names = ["AARON","ALEXA","BETTY","BILL","CAROL","COREY","DIANNE",
                "DYLAN","ELIZA","ETHAN","FRANK","FRANNIE","GILDENSTERN","GEORGIA",
                "HIDALGO","HAMLET","ISABELLE","ISAAC","JOHN","JENNA","KIT",
                "KATE","LAURA","LIAM","MALCOLM","MATHILDA","NAIOMI","NATHAN",
                "OREK","OTHELLO","PAUL","PRINCE","QUINCY","QUINN","ROSENCRANTZ",
                "RYAN","SAM","SHIRLEY","TINA","TOM","ULYSSES","UGENE","VANESSA",
                "VING","WALDO","WITT","XANDER","XENA","YOLANDA","YVETTE",
                "ZACH","ZIM"]
        use = ["MARY"]
        for i in xrange(21):
            use.append(names.pop(random.randint(0,len(names)-1)))
        use.sort()
        self.names = use
        self.guess = 5
        
    def askName(self):
        if self.grid[self.py][self.px].getType() != "DESK":
            return None;
        num = self.py-2
        #TODO animate the desk turning over
        if use[num]=="MARY":
            raise VictoryException()
        else:
            self.guess -= 1
            if self.guess == 0:
                raise OutOfGuessException()
            return use[num]

    def getPlane(self):
        """This method sets the coordinates for a plane that has
        been added to the map from a working file.
        """
        return self.plane;

    def move(self, heading):
        valid = True;
        if heading==0:
            newx = self.px+1
            newy = self.py
            if newx >= self.width:
                raise InvalidMoveException()
        if heading==1:
            newx = self.px
            newy = self.py-1
            if newx < 0:
                raise InvalidMoveException()
        if heading==2:
            newx = self.px-1
            newy = self.py
            if newx < 0:
                raise InvalidMoveException()
        if heading==3:
            newx = self.px
            newy = self.py+1
            if newx >= self.height:
                raise InvalidMoveException()
        if self.grid[newy][newx].getType() == "WALL" \
                or self.grid[newy][newx].getType() == "ISLAND":
            raise InvalidMoveException()
        if self.grid[newy][newx].getType() == "GATE":
            #TODO
            #victory condition
            self.py = newy
            self.px = newx
            if self.dummy:
                raise VictoryException()
        self.py = newy
        self.px = newx
        #TODO update the map

    def check(heading):
        """returns a string representing the type of object in fron
        of the plane
        """
        if heading==0:
            return self.grid[self.px+1][self.py].getType()
        if heading==1:
            return self.grid[self.px][self.py-1].getType()
        if heading==2:
            return self.grid[self.px-1][self.py].getType()
        if heading==3:
            return self.grid[self.px][self.py+1].getType()


    def runLevelDummy(self, user_name):

        working = runBox.run(self.map_path, self.level, user_name)
        #working = self.sand.start(self.map_path)
        output = open("output.py","r")
        if working:
            import runLevel as run
            reload(run)
            for y in xrange(self.height):
                for x in xrange(self.width):
                    if(self.grid[y][x].getType()=="PLANE"):
                        self.py = y
                        self.px = x
            #establish the path to pass along to GUI
            self.dummy = True
            self.plane.setDummy(True)
            self.plane.setHeading(0)
            try:
                run.runLevel(self.plane)
            except CrashException:
                pass;
                #do nothing, these are just to keep the user
                #code from executing forever
            self.dummy = False
            self.plane.setDummy(False)
#        else:
            #display error message??
        #TODO get this working?
        return working;

    def getLevel(self):
        return self.plane.getMoves()



    def __str__(self):
        """
        __str__: TileMap -> String
        Consumes: TileMap (implicit argument)
        Produces: String representation of TileMap
        Purpose: printing
        """
        ret = "* " * (self.width+1) + '*\n'
        for i in xrange(self.height):
            line = "* "
            for j in xrange(self.width):
                line += self.grid[i][j].__str__() + " "
            line += "*\n"
            ret += line
        ret += "* " * (self.width+1) + '*\n'
        return ret

    def filetomap(self, path):
        """
        Consumes: a TileMap and a file with a representation
        of the map, which is parsed into a level
        Produces: A self.grid array of Tiles, filled according
        to the file
        Purpose: Level creation
        """
        mapfile = open(path, "r")
        strmap = []
        for line in mapfile:
            strmap.append(line)
        mapfile.close()
        self.height = len(strmap)
        self.width = len(strmap[0])-1
        for i in range(len(strmap)):
            temp  = strmap[i].strip()
            if len(temp) != self.width:
                raise InvalidMapFileException()
            strmap[i] = temp
        self.grid = [ [] for i in range(self.height)]
        for i in xrange(self.height):
            for j in xrange(self.width):
                self.grid[i].append(Tile(strmap[i][j]))
                a = Tile(strmap[i][j])
#        print self.__str__()
        
            
