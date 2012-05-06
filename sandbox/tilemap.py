#!/usr/bin/Python
import sys
sys.path.append('/home/ecacciat/GLIDE/sandbox');
import runBox
import random
import maze
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
        self.six = ["0","1","2","3","4","5","6","7","8","9","a",
                "b","c","d","e","f"]
        self.sixes = ["0000","0001","0010","0011","0100","0101","0110",
                "0111","1000","1001","1010","1011","1100","1101","1110","1111"]
        self.value = "NULL"
        if value in self.valid:
            self.value = value
        elif value in self.sixes:
            self.value = value
        elif value in self.six:
            for i in xrange(len(self.six)):
                if value == self.six[i]:
                    self.value = self.sixes[i]

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
        Does not work on level6
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

class Room(Tile):
    """Room class

    This is an extension of the standard tile, and used for creating
    the DFS level.  It includes a "visited" decorator and a list of
    neighboring rooms
    """
    def __init__(self, value="AIR"):
        super(Tile, self).__init__(value)
        self.marked = False
        self.neighbors = []

    def setMark(self, marker):
        self.marked = marker

    def isMarked(self):
        return self.marked

    def neighbors(self):
        return self.neighbors

    def setNeighbors(self, hood):
        self.neighbors = hood


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
        if self.level == 5:
            self.initBinary()
            #TODO randomized Binary search stuff
        elif self.level == 6:
            maze.create_maze()
            #TODO drunken walk stuff
        #sets the plane
        self.filetomap(map_path)
        if self.level == 6:
            self.hood()
	print self.grid[0][0].getType()
        found = False
        self.plane = Airplane(self)
        for y in xrange(self.height):
            for x in xrange(self.width):
                if(self.grid[y][x].getType()=="PLANE"):
                    found = True
                    self.py = y
                    self.px = x
        if self.level == 6:
	    found = True
            self.py = 0
            self.px = 0

        if found == False:
            raise NoPlaneException() #there wasn't a plane 

    def hood(self):
        """
        Fills in the neighbor lists for the Rooms on level 6.
        """
        for y in xrange(self.height):
            for x in xrange(self.width):
                buds = []
                r = self.grid[y][x].getType()
                e = True if (r[0] is "0") else False
                n = True if (r[3] is "0") else False
                w = True if (r[1] is "0") else False
                s = True if (r[2] is "0") else False
                if e:
                    buds.append(self.grid[y][x+1].getType())
                if n:
                    buds.append(self.grid[y-1][x].getType())
                if w:
                    buds.append(self.grid[y][x-1].getType())
                if s:
                    buds.append(self.grid[y+1][x].getType())
                r.setNeighbors(buds)

    
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
        for i in xrange(23):
            use.append(names.pop(random.randint(0,len(names)-1)))
        use.sort()
        self.names = use
        self.guess = 5
        
    def askDeskName(self, desknum):
        if self.grid[self.py+1][self.px].getType() != "DESK":
            return None;
        dist = 0
        if self.px < desknum:
            heading = 0
            dist = desknum-self.px
        elif self.px > desknum:
            heading = 2
            dist = self.px-desknum
        self.plane.setHeading(heading)
        for i in xrange(dist):
            self.plane.move()
        #plane should now be above the desk of number desknum
        #TODO animate the desk turning over
        self.plane.moveSet.append(8)
        if self.names[num]=="MARY":
            raise VictoryException()
        else:
            self.guess -= 1
            if self.guess == 0:
                raise OutOfGuessException()
            return self.names[num]

    def getPlane(self):
        """This method sets the coordinates for a plane that has
        been added to the map from a working file.
        """
        return self.plane;

    def move(self, heading):
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
        front = self.grid[newy][newx].getType()
        if front == "WALL" \
                or front == "ISLAND" \
                or front == "DESK":
            raise InvalidMoveException()
        if front == "GATE":
            #TODO
            #victory condition
            self.py = newy
            self.px = newx
            if self.dummy:
                raise VictoryException()
        self.py = newy
        self.px = newx
        #TODO update the map

    def getHead(self, room):
        """
        returns an int representing the heading the arg room
        is in from the current location of the plane.
        """
        if self.grid[self.py][self.px+1].getType() == room:
            return 0;
        if self.grid[self.py-1][self.px].getType() == room:
            return 1;
        if self.grid[self.py][self.px-1].getType() == room:
            return 2;
        if self.grid[self.py+1][self.px].getType() == room:
            return 3;

    def move6(self, heading):
        x = self.grid[self.py][self.px].getType()
        e = True if (x[0] is "0") else False
        n = True if (x[3] is "0") else False
        w = True if (x[1] is "0") else False
        s = True if (x[2] is "0") else False
        if heading==0:
            newx = self.px+1
            newy = self.py
            if not e:
                raise InvalidMoveException()
        elif heading==1:
            newx = self.px
            newy = self.py-1
            if not n:
                raise InvalidMoveException()
        elif heading==2:
            newx = self.px-1
            newy = self.py
            if not w:
                raise InvalidMoveException()
        elif heading==3:
            newx = self.px
            newy = self.py+1
            if not s:
                raise InvalidMoveException()
        if (newx==24) and (newy==9):
            #TODO
            #victory condition
            self.py = newy
            self.px = newx
            if self.dummy:
                raise VictoryException()
        self.py = newy
        self.px = newx
        
    def check6(self, heading):
        x = self.grid[self.py][self.px].getType()
        e = True if (x[0] is "0") else False
        n = True if (x[3] is "0") else False
        w = True if (x[1] is "0") else False
        s = True if (x[2] is "0") else False
        if heading==0:
            newx = self.px+1
            newy = self.py
            if not e:
                raise InvalidMoveException()
        if heading==1:
            newx = self.px
            newy = self.py-1
            if not n:
                raise InvalidMoveException()
        if heading==2:
            newx = self.px-1
            newy = self.py
            if not w:
                raise InvalidMoveException()
        if heading==3:
            newx = self.px
            newy = self.py+1
            if not s:
                raise InvalidMoveException()
        front = self.grid[newy][newx].getType()
        if front == "GATE":
            return "GATE"
        else:
            return "AIR"



    def check(self, heading):
        """returns a string representing the type of object in fron
        of the plane
        """
        if heading==0:
            newx = self.px+1
            newy = self.py
            if newx >= self.width:
                raise MapBorderException()
        if heading==1:
            newx = self.px
            newy = self.py-1
            if newy < 0:
                raise MapBorderException()
        if heading==2:
            newx = self.px-1
            newy = self.py
            if newx < 0:
                raise MapBorderException()
        if heading==3:
            newx = self.px
            newy = self.py+1
            if newy >= self.height:
                raise MapBorderException()
        return self.grid[newy][newx].getType()

    def runLevelDummy(self, user_name):

        working = runBox.run(self.map_path, self.level, user_name)
        #working = self.sand.start(self.map_path)
        output = open("output.py","r")
        if working:
            if self.level == 6:
                maze.create_maze()
                self.filetomap(self.map_path)
            elif self.level == 5:
                self.initBinary()
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
                print len(temp), self.width
                raise InvalidMapFileException()
            strmap[i] = temp
        self.grid = [ [] for i in range(self.height)]
        for i in xrange(self.height):
            for j in xrange(self.width):
                if self.level == 6:
                    a = Room(strmap[i][j])
                else:
                    a = Tile(strmap[i][j])
                self.grid[i].append(a)
#        print self.__str__()
        
            
