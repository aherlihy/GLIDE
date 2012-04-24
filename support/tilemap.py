#!/usr/bin/Python

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


class Tile:
    """Map Tile Class

    This object represents a single tile of the map we will be displaying

    Author: jwoberbe
    Date:3.19.12
    """

    def __init__(self, value= "AIR") :
        self.valid = ["AIR","CLOUD","GATE","PLANE"]
        self.bitval = ["0","1","X","P"]
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
            return "0";
        if self.value == "CLOUD":
            return "1";
        if self.value == "GATE":
            return "X";
        if self.value == "PLANE":
            return "P";

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

    def __init__(self):
        #fix init to a set size, and edge in with clouds
        self.height = 8
        self.width = 12 #??
        self.grid = [ [] for i in range(self.height)]
        for row in self.grid:
            for j in xrange(self.width):
                row.append(Tile())

    """
    The following methods are used for navigating the plane around the
    map.
    """
    def setPlane(self):
        """This method sets the coordinates for a plane that has
        been added to the map from a working file.
        """
        found = False
        for y in xrange(self.height):
            for x in xrange(self.width):
                if(self.grid[y][x].getType()=="PLANE"):
                    found = True
                    self.py = y
                    self.px = x
        if found == False:
            raise NoPlaneException()


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
        if self.grid[newy][newx].getType() == "CLOUD":
            raise InvalidMoveException()
        if self.grid[newy][newx].getType() == "GATE":
            #TODO
            #victory condition
            print "We won!!"
            return;
        temp = self.grid[self.py][self.px]
        self.grid[self.py][self.px] = self.grid[newy][newx]
        self.grid[newy][newx] = temp
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


    def runLevel(self, levelnum):
        pathname = "level"+str(levelnum)
        exec pathname
        #TODO get this working?



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
        print self.__str__()
        
            
