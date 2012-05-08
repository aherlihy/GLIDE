#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import time, cmath, math, tkFont, thread, re, random
import Tkinter as tk

TILE_WIDTH = 48
TILE_HEIGHT = 44
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 440
NUM_TILES_WIDE = CANVAS_WIDTH/TILE_WIDTH   # 25
NUM_TILES_HIGH = CANVAS_HEIGHT/TILE_HEIGHT # 10
PLANE_WIDTH = 55
PLANE_HEIGHT = 39

DIR_NORTH = 0
DIR_WEST = 90
DIR_SOUTH = 180
DIR_EAST = 270

# firework colors
RED1 = '#FF0000'
RED2 = '#FF7777'
RED3 = '#FFCCCC'

GOLD1 = '#FFD700'
GOLD2 = '#FFE744'
GOLD3 = '#FFF788'

GREEN1 = '#32CD32'
GREEN2 = '#70ED70'
GREEN3 = '#A0FDA0'

TURQ1 = '#00CED1'
TURQ2 = '#50DEE1'
TURQ3 = '#A0EEF1'

PURPLE1 = '#9932CC'
PURPLE2 = '#C082DD'
PURPLE3 = '#E0B2EE'

class Painter:

    def __init__(self, canvas, charArray):

        self.canvas = canvas
        self.paintMap(charArray)

        self.waitingFont = tkFont.Font(family="Pupcat", size=20, weight=tkFont.BOLD)
        self.dialogFont = tkFont.Font(family="Pupcat", size=12, weight=tkFont.BOLD)

        self.waitingOutline = self.canvas.create_rectangle(460, 90, 720, 130, fill="Yellow",
                                                           dash='3', width=2, state=HIDDEN)
        self.waitingText = self.canvas.create_text(588, 110, font=self.waitingFont, text="Checking your code...", state=HIDDEN)
        self.numBalloons = 0
        self.balloonList = []
        
        self.numNames = 0
        
        self.SPEED = .007
	self.ROT_SPEED = .003


    def setSpeeds(self, speed, rotSpeed):
	self.SPEED = speed
	self.ROT_SPEED = rotSpeed


    def paintMap(self, charArray):
	""" Create a map of tiles based on a character array. The following characters are valid:
	    B - blank (air)
	    W - wall (cloud)
	    I - island (cloud)
	"""

        img_wall0001 = Image.open("Graphics/Tiles/Walls/0001_wall.png")
        img_wall0010 = Image.open("Graphics/Tiles/Walls/0010_wall.png")
        img_wall0011 = Image.open("Graphics/Tiles/Walls/0011_wall.png")
        img_wall0100 = Image.open("Graphics/Tiles/Walls/0100_wall.png")
        img_wall0101 = Image.open("Graphics/Tiles/Walls/0101_wall.png")
        img_wall0110 = Image.open("Graphics/Tiles/Walls/0110_wall.png")
        img_wall0111 = Image.open("Graphics/Tiles/Walls/0111_wall.png")
        img_wall1000 = Image.open("Graphics/Tiles/Walls/1000_wall.png")
        img_wall1001 = Image.open("Graphics/Tiles/Walls/1001_wall.png")
        img_wall1010 = Image.open("Graphics/Tiles/Walls/1010_wall.png")
        img_wall1011 = Image.open("Graphics/Tiles/Walls/1011_wall.png")
        img_wall1100 = Image.open("Graphics/Tiles/Walls/1100_wall.png")
        img_wall1101 = Image.open("Graphics/Tiles/Walls/1101_wall.png")
        img_wall1110 = Image.open("Graphics/Tiles/Walls/1110_wall.png")
        img_wall1111 = Image.open("Graphics/Tiles/Walls/1111_wall.png")

        img_air = Image.open("Graphics/Tiles/air.png")

        img_island0000 = Image.open("Graphics/Tiles/Islands/0000_island.png")
        img_island0011 = Image.open("Graphics/Tiles/Islands/0011_island.png")
        img_island0110 = Image.open("Graphics/Tiles/Islands/0110_island.png")
        img_island0111 = Image.open("Graphics/Tiles/Islands/0111_island.png")
        img_island1001 = Image.open("Graphics/Tiles/Islands/1001_island.png")
        img_island1011 = Image.open("Graphics/Tiles/Islands/1011_island.png")
        img_island1100 = Image.open("Graphics/Tiles/Islands/1100_island.png")
        img_island1101 = Image.open("Graphics/Tiles/Islands/1101_island.png")
        img_island1110 = Image.open("Graphics/Tiles/Islands/1110_island.png")
        img_island1111 = Image.open("Graphics/Tiles/Islands/1111_island.png")
        img_islandSEcorner = Image.open("Graphics/Tiles/Islands/SEcorner_island.png")
        img_islandSWcorner = Image.open("Graphics/Tiles/Islands/SWcorner_island.png")
        img_islandNEcorner = Image.open("Graphics/Tiles/Islands/NEcorner_island.png")
        img_islandNWcorner = Image.open("Graphics/Tiles/Islands/NWcorner_island.png")

        img_maze1 = Image.open("Graphics/Tiles/Maze/maze1.png")
        img_maze2 = Image.open("Graphics/Tiles/Maze/maze2.png")
        img_maze3 = Image.open("Graphics/Tiles/Maze/maze3.png")
        img_maze4 = Image.open("Graphics/Tiles/Maze/maze4.png")
        img_maze5 = Image.open("Graphics/Tiles/Maze/maze5.png")
        img_maze6 = Image.open("Graphics/Tiles/Maze/maze6.png")
        img_maze7 = Image.open("Graphics/Tiles/Maze/maze7.png")
        img_maze8 = Image.open("Graphics/Tiles/Maze/maze8.png")
        img_maze9 = Image.open("Graphics/Tiles/Maze/maze9.png")
        img_mazea = Image.open("Graphics/Tiles/Maze/mazea.png")
        img_mazeb = Image.open("Graphics/Tiles/Maze/mazeb.png")
        img_mazec = Image.open("Graphics/Tiles/Maze/mazec.png")
        img_mazed = Image.open("Graphics/Tiles/Maze/mazed.png")
        img_mazee = Image.open("Graphics/Tiles/Maze/mazee.png")
        img_mazef = Image.open("Graphics/Tiles/Maze/mazef.png")

        img_goal = Image.open("Graphics/Tiles/goal.png")
        
        img_brick = Image.open("Graphics/Tiles/Recess/brick.png")
        img_head1 = Image.open("Graphics/Tiles/Recess/head1a.png")
        img_head2 = Image.open("Graphics/Tiles/Recess/head2a.png")
        img_head3 = Image.open("Graphics/Tiles/Recess/head3a.png")
        img_head4 = Image.open("Graphics/Tiles/Recess/head4a.png")
        img_head5 = Image.open("Graphics/Tiles/Recess/head5a.png")
        img_head6 = Image.open("Graphics/Tiles/Recess/head6a.png")
        img_head7 = Image.open("Graphics/Tiles/Recess/head7a.png")
        img_head8 = Image.open("Graphics/Tiles/Recess/head8a.png")
        img_head9 = Image.open("Graphics/Tiles/Recess/head9a.png")
        img_head10 = Image.open("Graphics/Tiles/Recess/head10a.png")
        
        img_floor = Image.open("Graphics/Tiles/Classroom/floor.png")
        img_desk1 = Image.open("Graphics/Tiles/Classroom/desk1.png")
        img_desk2 = Image.open("Graphics/Tiles/Classroom/desk2.png")
        img_desk3 = Image.open("Graphics/Tiles/Classroom/desk3.png")
        img_desk4 = Image.open("Graphics/Tiles/Classroom/desk4.png")
        img_desk5 = Image.open("Graphics/Tiles/Classroom/desk5.png")
        img_desk6 = Image.open("Graphics/Tiles/Classroom/desk6.png")
        img_desk7 = Image.open("Graphics/Tiles/Classroom/desk7.png")
        img_desk8 = Image.open("Graphics/Tiles/Classroom/desk8.png")
        img_desk9 = Image.open("Graphics/Tiles/Classroom/desk9.png")
        img_desk10 = Image.open("Graphics/Tiles/Classroom/desk10.png")
        img_teacher = Image.open("Graphics/Tiles/Classroom/teacher.png")
        
        img_bubble1 = Image.open("Graphics/bubble1.png")
        img_bubble2 = Image.open("Graphics/bubble2.png")
        img_bubble3 = Image.open("Graphics/bubble3.png")

        self.wall0001 = ImageTk.PhotoImage(img_wall0001)
        self.wall0010 = ImageTk.PhotoImage(img_wall0010)
        self.wall0011 = ImageTk.PhotoImage(img_wall0011)
        self.wall0100 = ImageTk.PhotoImage(img_wall0100)
        self.wall0101 = ImageTk.PhotoImage(img_wall0101)
        self.wall0110 = ImageTk.PhotoImage(img_wall0110)
        self.wall0111 = ImageTk.PhotoImage(img_wall0111)
        self.wall1000 = ImageTk.PhotoImage(img_wall1000)
        self.wall1001 = ImageTk.PhotoImage(img_wall1001)
        self.wall1010 = ImageTk.PhotoImage(img_wall1010)
        self.wall1011 = ImageTk.PhotoImage(img_wall1011)
        self.wall1100 = ImageTk.PhotoImage(img_wall1100)
        self.wall1101 = ImageTk.PhotoImage(img_wall1101)
        self.wall1110 = ImageTk.PhotoImage(img_wall1110)
        self.wall1111 = ImageTk.PhotoImage(img_wall1111)

        self.air = ImageTk.PhotoImage(img_air)

        self.island0000 = ImageTk.PhotoImage(img_island0000)
        self.island0011 = ImageTk.PhotoImage(img_island0011)
        self.island0110 = ImageTk.PhotoImage(img_island0110)
        self.island0111 = ImageTk.PhotoImage(img_island0111)
        self.island1001 = ImageTk.PhotoImage(img_island1001)
        self.island1011 = ImageTk.PhotoImage(img_island1011)
        self.island1100 = ImageTk.PhotoImage(img_island1100)
        self.island1101 = ImageTk.PhotoImage(img_island1101)
        self.island1110 = ImageTk.PhotoImage(img_island1110)
        self.island1111 = ImageTk.PhotoImage(img_island1111)
        self.islandSEcorner = ImageTk.PhotoImage(img_islandSEcorner)
        self.islandSWcorner = ImageTk.PhotoImage(img_islandSWcorner)
        self.islandNEcorner = ImageTk.PhotoImage(img_islandNEcorner)
        self.islandNWcorner = ImageTk.PhotoImage(img_islandNWcorner)
        
        self.maze1 = ImageTk.PhotoImage(img_maze1)
        self.maze2 = ImageTk.PhotoImage(img_maze2)
        self.maze3 = ImageTk.PhotoImage(img_maze3)
        self.maze4 = ImageTk.PhotoImage(img_maze4)
        self.maze5 = ImageTk.PhotoImage(img_maze5)
        self.maze6 = ImageTk.PhotoImage(img_maze6)
        self.maze7 = ImageTk.PhotoImage(img_maze7)
        self.maze8 = ImageTk.PhotoImage(img_maze8)
        self.maze9 = ImageTk.PhotoImage(img_maze9)
        self.mazea = ImageTk.PhotoImage(img_mazea)
        self.mazeb = ImageTk.PhotoImage(img_mazeb)
        self.mazec = ImageTk.PhotoImage(img_mazec)
        self.mazed = ImageTk.PhotoImage(img_mazed)
        self.mazee = ImageTk.PhotoImage(img_mazee)
        self.mazef = ImageTk.PhotoImage(img_mazef)

        self.goal = ImageTk.PhotoImage(img_goal)
        
        self.brick = ImageTk.PhotoImage(img_brick)
        self.head1 = ImageTk.PhotoImage(img_head1)
        self.head2 = ImageTk.PhotoImage(img_head2)
        self.head3 = ImageTk.PhotoImage(img_head3)
        self.head4 = ImageTk.PhotoImage(img_head4)
        self.head5 = ImageTk.PhotoImage(img_head5)
        self.head6 = ImageTk.PhotoImage(img_head6)
        self.head7 = ImageTk.PhotoImage(img_head7)
        self.head8 = ImageTk.PhotoImage(img_head8)
        self.head9 = ImageTk.PhotoImage(img_head9)
        self.head10 = ImageTk.PhotoImage(img_head10)
        
        self.floor = ImageTk.PhotoImage(img_floor)
        self.desk1 = ImageTk.PhotoImage(img_desk1)
        self.desk2 = ImageTk.PhotoImage(img_desk2)
        self.desk3 = ImageTk.PhotoImage(img_desk3)
        self.desk4 = ImageTk.PhotoImage(img_desk4)
        self.desk5 = ImageTk.PhotoImage(img_desk5)
        self.desk6 = ImageTk.PhotoImage(img_desk6)
        self.desk7 = ImageTk.PhotoImage(img_desk7)
        self.desk8 = ImageTk.PhotoImage(img_desk8)
        self.desk9 = ImageTk.PhotoImage(img_desk9)
        self.desk10 = ImageTk.PhotoImage(img_desk10)
        self.teacher = ImageTk.PhotoImage(img_teacher)
        
        self.bubble1 = ImageTk.PhotoImage(img_bubble1)
        self.bubble2 = ImageTk.PhotoImage(img_bubble2)
        self.bubble3 = ImageTk.PhotoImage(img_bubble3)
        
        maze = False
        hexPattern = re.compile("[\da-g]")
        
        self.planeX = 0
        self.planeY = 0
        
        teacherLoc = None
        paintFloor = False

        for row in range(0, NUM_TILES_HIGH):

            for col in range(0, NUM_TILES_WIDE):

                x = col*TILE_WIDTH
                y = row*TILE_HEIGHT

                # air / floor
                if charArray[row][col] == 'A':
                    if paintFloor:
			self.canvas.create_image(x, y, image=self.floor, anchor=NW)
	            else: 
			self.canvas.create_image(x, y, image=self.air, anchor=NW)

                # cloud wall
                elif charArray[row][col] == 'W':
                    self.canvas.create_image(x, y, image=(self.makeWall(charArray, row, col)), anchor=NW)

                # cloud island
                elif charArray[row][col] == 'I':
                    self.canvas.create_image(x, y, image=(self.makeIsland(charArray, row, col)), anchor=NW)

                # goal 
                elif charArray[row][col] == 'G':
		    self.canvas.create_image(x, y, image=self.air, anchor=NW)
                    self.canvas.create_image(x, y, image=self.goal, anchor=NW)

                # student
                elif charArray[row][col] == 'S':
                    self.canvas.create_image(x, y, image=self.createStudent(), anchor=NW)

                # brick
                elif charArray[row][col] == 'B':
                    self.canvas.create_image(x, y, image=self.brick, anchor=NW)
                    paintFloor = True

		# desk
		elif charArray[row][col] == 'D':
		    self.canvas.create_image(x, y, image=self.createDesk(), anchor=NW)

                # teacher
		elif charArray[row][col] == 'T':
		    self.canvas.create_image(x, y, image=self.floor, anchor=NW)
		    teacherLoc = (x, y)

                # plane - set plane here and make square underneath air
                elif charArray[row][col] == 'P':
		    if teacherLoc is not None:
			self.canvas.create_image(x, y, image=self.floor, anchor=NW)
                    else:
		        self.canvas.create_image(x, y, image=self.air, anchor=NW)
		    self.planeX = x
		    self.planeY = y

                # maze
                elif hexPattern.match(charArray[row][col]) != None:
		    self.canvas.create_image(x, y, image=(self.makeMaze(charArray, row, col)), anchor=NW)
		    maze = True

                else:
                    print "Unrecognized character ", charArray[row][col], " in map file."
                    self.canvas.create_image(x, y, image=self.air, anchor=NW)

        # if we have a teacher's desk in this level, draw it on top of other stuff
        if teacherLoc is not None:
	    self.canvas.create_image(teacherLoc[0], teacherLoc[1], image=self.teacher, anchor=SE)

        if maze:
	    self.canvas.create_image(NUM_TILES_WIDE*TILE_WIDTH, NUM_TILES_HIGH*TILE_HEIGHT, image=self.goal, anchor=SE)

        # after all tiles have been set, draw the plane so it's on top of everything else
        self.initPlane()


    def makeWall(self, charArray, row, col):
        """ Called when we get a wall character in the charArray. Examines the cells
            to the top, bottom, left, and right of the cell at (row, col) to determine
            which kind of wall to paint. """

        m = len(charArray)
        n = len(charArray[0])

        # make list of walls where index in list corresponds to decimal value of
        # the binary that describes the wall, where (top, right, btm, left) ->
        # binary (xxxx)
        walls = [     self.air, self.wall0001, self.wall0010, self.wall0011,
                 self.wall0100, self.wall0101, self.wall0110, self.wall0111,
                 self.wall1000, self.wall1001, self.wall1010, self.wall1011,
                 self.wall1100, self.wall1101, self.wall1110, self.wall1111]

        # compute binary value of wall depending on its neighbors
        wallBin = ["0", "0", "0", "0"]    # default values for when a cell is off the edge

        # top
        if (row - 1) >= 0:
            if charArray[row - 1][col] == 'W':
                wallBin[3] = "1"

        # right
        if (col + 1) <= (n - 1):
            if charArray[row][col + 1] == 'W':
                wallBin[2] = "1"

        # bottom
        if (row + 1) <= (m - 1):
            if charArray[row + 1][col] == 'W':
                wallBin[1] = "1"

        # left
        if (col - 1) >= 0:
            if charArray[row][col - 1] == 'W':
                wallBin[0] = "1"

        # use the string os 0s and 1s a binary index into the array, and return the correct wall
        wallType = int(str(wallBin[3] + wallBin[2] + wallBin[1] + wallBin[0]), 2)
        return walls[wallType]


    def makeIsland(self, charArray, row, col):
        """ Called when we get an island character in the charArray. Examines the cells
            to the top, bottom, left, and right of the cell at (row, col) to determine
            which kind of island to paint. """

        m = len(charArray)
        n = len(charArray[0])

        # make list of islands where index in list corresponds to decimal value of
        # the binary that describes the wall, where (top, right, btm, left) ->
        # binary (xxxx). 0s indicate non-existent types of island (i.e. invalid 
        # map file)
        islands = [self.island0000,     0,                   0,                   self.island0011,
                   0,                   0,                   self.island0110,     self.island0111,
                   0,                   self.island1001,     0,                   self.island1011,
                   self.island1100,     self.island1101,     self.island1110,     self.island1111]

        # compute binary value of island depending on its neighbors
        islandBin = ["0", "0", "0", "0"]    # default values for when a cell is off the edge

        # top
        if (row - 1) >= 0:
            if charArray[row - 1][col] == 'I':
                islandBin[3] = "1"

        # right
        if (col + 1) <= (n - 1):
            if charArray[row][col + 1] == 'I':
                islandBin[2] = "1"

        # bottom
        if (row + 1) <= (m - 1):
            if charArray[row + 1][col] == 'I':
                islandBin[1] = "1"

        # left
        if (col - 1) >= 0:
            if charArray[row][col - 1] == 'I':
                islandBin[0] = "1"

        # corners
        if islandBin == ["1", "1", "1", "1"]:
	    if (row - 1 >= 0) and (col - 1 >= 0) and charArray[row - 1][col - 1] != 'I':
		return self.islandNWcorner
	    elif (row - 1 >= 0) and (col + 1 <= n-1) and charArray[row - 1][col + 1] != 'I':
		return self.islandNEcorner
	    elif (row + 1 <= m-1) and (col - 1 >= 0) and charArray[row + 1][col - 1] != 'I':
		return self.islandSWcorner
	    elif (row + 1 <= m-1) and (col + 1 <= n-1) and charArray[row + 1][col + 1] != 'I':
		return self.islandSEcorner

        # use the string os 0s and 1s a binary index into the array, and return the correct wall
        islandType = int(str(islandBin[3] + islandBin[2] + islandBin[1] + islandBin[0]), 2)
        if islands[islandType] == 0:
	    print "Invalid use of islands in map file. Filling in with air spaces."
	    return self.air
        return islands[islandType]


    def makeMaze(self, charArray, row, col):
	
	mazePieces = [self.air,   self.maze1, self.maze2, self.maze3,
	              self.maze4, self.maze5, self.maze6, self.maze7,
	              self.maze8, self.maze9, self.mazea, self.mazeb,
	              self.mazec, self.mazed, self.mazee, self.mazef]
	
	hexChar = charArray[row][col]
	if hexChar == 'g':
	    return self.island1111
	else:
	    decValue = int(hexChar, 16)
	    return mazePieces[decValue]


    def createStudent(self):
	heads = [self.head1, self.head2, self.head3, self.head4, self.head5,
	         self.head6, self.head7, self.head8, self.head9, self.head10]

	num = random.randint(0, 9)
	return heads[num]


    def createDesk(self):
	desks = [self.desk1, self.desk2, self.desk3, self.desk4, self.desk5,
	         self.desk6, self.desk7, self.desk8, self.desk9, self.desk10]

	num = random.randint(0, 9)
	return desks[num]


    def initPlane(self):
        img = Image.open("Graphics/plane.png")
        imgRotated = img.rotate(DIR_EAST)
        self.planeImg = ImageTk.PhotoImage(imgRotated)
        self.plane = self.canvas.create_image(self.planeX, self.planeY, image=self.planeImg, anchor=NW, tags="plane")
        self.planeRotDeg = DIR_EAST   # keep track of the orientation of the plane
        self.canvas.coords("plane", self.planeX, self.planeY)
        self.canvas.update()


    def showCheckingText(self):
	self.canvas.itemconfig(self.waitingOutline, state=NORMAL)
        self.canvas.itemconfig(self.waitingText, state=NORMAL)


    def hideCheckingText(self):
	self.canvas.itemconfig(self.waitingOutline, state=HIDDEN)
	self.canvas.itemconfig(self.waitingText, state=HIDDEN)


    def movePlaneEast(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_EAST:
	    if self.planeRotDeg == DIR_NORTH:   # turn counterclockwise
	        self.rotatePlaneClockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneCounterclockwise(abs(self.planeRotDeg - DIR_EAST))
	self.planeRotDeg = DIR_EAST

	for i in range(0, TILE_WIDTH):
	    time.sleep(self.SPEED)
	    self.canvas.move("plane", 1, 0)
	    self.canvas.update()


    def movePlaneWest(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_WEST:
	    if self.planeRotDeg == DIR_NORTH:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_WEST))
	self.planeRotDeg = DIR_WEST

	for i in range(0, TILE_WIDTH):
	    time.sleep(self.SPEED)
	    self.canvas.move("plane", -1, 0)
	    self.canvas.update()


    def movePlaneNorth(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_NORTH:
	    if self.planeRotDeg == DIR_EAST:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_NORTH))
	self.planeRotDeg = DIR_NORTH

	for i in range(0, TILE_HEIGHT):
	    time.sleep(self.SPEED)
	    self.canvas.move("plane", 0, -1)
	    self.canvas.update()


    def movePlaneSouth(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_SOUTH:
	    if self.planeRotDeg == DIR_EAST:   # turn clockwise
	        self.rotatePlaneClockwise(90)
	    else:       # turn counterclockwise
		self.rotatePlaneCounterclockwise(abs(self.planeRotDeg - DIR_SOUTH))
	self.planeRotDeg = DIR_SOUTH

	for i in range(0, TILE_HEIGHT):
	    time.sleep(self.SPEED)
	    self.canvas.move("plane", 0, 1)
	    self.canvas.update()


    def rotatePlaneClockwise(self, numDegrees):
	x, y = self.canvas.coords("plane")
	for deg in range(0, numDegrees):
	    time.sleep(self.ROT_SPEED)
	    self.canvas.delete("plane")
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg - deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(x, y, image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = (self.planeRotDeg - numDegrees) % 360


    def rotatePlaneCounterclockwise(self, numDegrees):
	x, y = self.canvas.coords("plane")
	for deg in range(0, numDegrees):
	    time.sleep(self.ROT_SPEED)
	    self.canvas.delete("plane")
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg + deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(x, y, image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = (self.planeRotDeg + numDegrees) % 360


    def takeRightTurnSouth(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_EAST:
	    if self.planeRotDeg == DIR_NORTH:
	        self.rotatePlaneClockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneCounterclockwise(abs(self.planeRotDeg - DIR_EAST))
	
	startx, starty = self.canvas.coords("plane")  # starting position
	x = 0.0
	deg = 0
	while x <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    x += 1.0/TILE_WIDTH
	    y = x*x
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 90.0/TILE_WIDTH
	    self.canvas.delete("plane")    # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg - deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx + x * TILE_WIDTH, starty + y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = DIR_SOUTH


    def takeRightTurnNorth(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_WEST:
	    if self.planeRotDeg == DIR_NORTH:   # turn counterlockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_WEST))

	startx, starty = self.canvas.coords("plane")  # starting position
	x = 0.0
	deg = 0
	while x <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    x += 1.0/TILE_WIDTH
	    y = x*x
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 90.0/TILE_WIDTH
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg - deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx - x * TILE_WIDTH, starty - y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
        self.planeRotDeg = DIR_NORTH

    def takeRightTurnEast(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_NORTH:
	    if self.planeRotDeg == DIR_EAST:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_NORTH))

	startx, starty = self.canvas.coords("plane")  # starting position
	y = 0.0
	deg = 0
	while y <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    y += 1.0/TILE_HEIGHT
	    x = y*y
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 90.0/TILE_HEIGHT
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg - deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx + x * TILE_WIDTH, starty - y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = DIR_EAST


    def takeRightTurnWest(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_SOUTH:
	    if self.planeRotDeg == DIR_WEST:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_SOUTH))

	startx, starty = self.canvas.coords("plane")  # starting position
	y = 0.0
	deg = 0
	while y <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    y += 1.0/TILE_HEIGHT
	    x = y*y
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 90.0/TILE_HEIGHT
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg - deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx - x * TILE_WIDTH, starty + y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = DIR_WEST


    def takeLeftTurnSouth(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_WEST:
	    if self.planeRotDeg == DIR_NORTH:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_WEST))

	startx, starty = self.canvas.coords("plane")  # starting position
	x = 0.0
	deg = 0
	while x <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    x += 1.0/TILE_WIDTH
	    y = x*x
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 90.0/TILE_WIDTH
	    self.canvas.delete("plane")    # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg + deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx - x * TILE_WIDTH, starty + y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = DIR_SOUTH


    def takeLeftTurnNorth(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_EAST:
	    if self.planeRotDeg == DIR_SOUTH:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(360 - abs(self.planeRotDeg - DIR_EAST))

	startx, starty = self.canvas.coords("plane")  # starting position
	x = 0.0
	deg = 0
	while x <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    x += 1.0/TILE_WIDTH
	    y = x*x
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 90.0/TILE_WIDTH
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg + deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx + x * TILE_WIDTH, starty - y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
        self.planeRotDeg = DIR_NORTH

    def takeLeftTurnEast(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_SOUTH:
	    if self.planeRotDeg == DIR_WEST:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_SOUTH))

	startx, starty = self.canvas.coords("plane")  # starting position
	y = 0.0
	deg = 0
	while y <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    y += 1.0/TILE_HEIGHT
	    x = y*y
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 90.0/TILE_HEIGHT
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg + deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx + x * TILE_WIDTH, starty + y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = DIR_EAST


    def takeLeftTurnWest(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_NORTH:
	    if self.planeRotDeg == DIR_EAST:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_NORTH))

	startx, starty = self.canvas.coords("plane")  # starting position
	y = 0.0
	deg = 0
	while y <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    y += 1.0/TILE_HEIGHT
	    x = y*y
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 90.0/TILE_HEIGHT
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg + deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx - x * TILE_WIDTH, starty - y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = DIR_WEST


    def sBendEastNorth(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_EAST:
	    if self.planeRotDeg == DIR_SOUTH:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(360 - abs(self.planeRotDeg - DIR_EAST))

        startx, starty = self.canvas.coords("plane")  # starting position
	x = 0.0
	deg = 0
	while x <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    x += 1.0/TILE_WIDTH
	    y = (x*x)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_WIDTH
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg + deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx + x * TILE_WIDTH, starty - y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
        self.planeRotDeg = 315

	startx, starty = self.canvas.coords("plane")  # starting position
	x = 0.0
	deg = 0
	while x <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    x += 1.0/TILE_HEIGHT
	    y = math.sqrt(x)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_HEIGHT
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg - deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx + x * TILE_WIDTH, starty - y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = DIR_EAST
	

    def sBendEastSouth(self):
        # make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_EAST:
	    if self.planeRotDeg == DIR_SOUTH:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(360 - abs(self.planeRotDeg - DIR_EAST))
	
        startx, starty = self.canvas.coords("plane")  # starting position
	x = 0.0
	deg = 0
	while x <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    x += 1.0/TILE_WIDTH
	    y = (x*x)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_WIDTH
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg - deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx + x * TILE_WIDTH, starty + y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
        self.planeRotDeg = 225

	startx, starty = self.canvas.coords("plane")  # starting position
	x = 0.0
	deg = 0
	while x <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    x += 1.0/TILE_HEIGHT
	    y = math.sqrt(x)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_HEIGHT
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg + deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx + x * TILE_WIDTH, starty + y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = DIR_EAST


    def sBendWestNorth(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_WEST:
	    if self.planeRotDeg == DIR_NORTH:   # turn counterlockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_WEST))

	startx, starty = self.canvas.coords("plane")  # starting position
	x = 0.0
	deg = 0
	while x <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    x += 1.0/TILE_WIDTH
	    y = (x*x)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_WIDTH
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg - deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx - x * TILE_WIDTH, starty - y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	
	self.planeRotDeg = 45
	
	startx, starty = self.canvas.coords("plane")  # starting position
	x = 0.0
	deg = 0
	while x <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    x += 1.0/TILE_HEIGHT
	    y = math.sqrt(x)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_HEIGHT
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg + deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx - x * TILE_WIDTH, starty - y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = DIR_WEST


    def sBendWestSouth(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_WEST:
	    if self.planeRotDeg == DIR_NORTH:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_WEST))

	startx, starty = self.canvas.coords("plane")  # starting position
	x = 0.0
	deg = 0
	while x <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    x += 1.0/TILE_WIDTH
	    y = (x*x)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_WIDTH
	    self.canvas.delete("plane")    # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg + deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx - x * TILE_WIDTH, starty + y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = 135
	
	startx, starty = self.canvas.coords("plane")  # starting position
	x = 0.0
	deg = 0
	while x <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    x += 1.0/TILE_HEIGHT
	    y = math.sqrt(x)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_HEIGHT
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg - deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx - x * TILE_WIDTH, starty + y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = DIR_WEST


    def sBendNorthEast(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_NORTH:
	    if self.planeRotDeg == DIR_EAST:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_NORTH))

	startx, starty = self.canvas.coords("plane")  # starting position
	y = 0.0
	deg = 0
	while y <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    y += 1.0/TILE_HEIGHT
	    x = (y*y)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_HEIGHT
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg - deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx + x * TILE_WIDTH, starty - y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = 315

        startx, starty = self.canvas.coords("plane")  # starting position
	y = 0.0
	deg = 0
	while y <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    y += 1.0/TILE_WIDTH
	    x = math.sqrt(y)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_WIDTH
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg + deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx + x * TILE_WIDTH, starty - y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
        self.planeRotDeg = DIR_NORTH


    def sBendNorthWest(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_NORTH:
	    if self.planeRotDeg == DIR_EAST:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_NORTH))

	startx, starty = self.canvas.coords("plane")  # starting position
	y = 0.0
	deg = 0
	while y <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    y += 1.0/TILE_HEIGHT
	    x = (y*y)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_HEIGHT
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg + deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx - x * TILE_WIDTH, starty - y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
        self.planeRotDeg = 45
        
        startx, starty = self.canvas.coords("plane")  # starting position
	y = 0.0
	deg = 0
	while y <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    y += 1.0/TILE_WIDTH
	    x = math.sqrt(y)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_WIDTH
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg - deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx - x * TILE_WIDTH, starty - y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
        self.planeRotDeg = DIR_NORTH


    def sBendSouthEast(self):
	# make sure we're facing in the correct direction first
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_SOUTH:
	    if self.planeRotDeg == DIR_WEST:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_SOUTH))

	startx, starty = self.canvas.coords("plane")  # starting position
	y = 0.0
	deg = 0
	while y <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    y += 1.0/TILE_HEIGHT
	    x = (y*y)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_HEIGHT
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg + deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx + x * TILE_WIDTH, starty + y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = 225
	
	startx, starty = self.canvas.coords("plane")  # starting position
	y = 0.0
	deg = 0
	while y <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    y += 1.0/TILE_WIDTH
	    x = math.sqrt(y)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_WIDTH
	    self.canvas.delete("plane")    # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg - deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx + x * TILE_WIDTH, starty + y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = DIR_SOUTH


    def sBendSouthWest(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_SOUTH:
	    if self.planeRotDeg == DIR_WEST:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_SOUTH))

	startx, starty = self.canvas.coords("plane")  # starting position
	y = 0.0
	deg = 0
	while y <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    y += 1.0/TILE_HEIGHT
	    x = (y*y)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_HEIGHT
	    self.canvas.delete("plane")   # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg - deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx - x * TILE_WIDTH, starty + y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = 135
	
	startx, starty = self.canvas.coords("plane")  # starting position
	y = 0.0
	deg = 0
	while y <= 1.0:
	    time.sleep(self.SPEED)

	    # calculate values for a hyperbola with a scale of 1
	    y += 1.0/TILE_WIDTH
	    x = math.sqrt(y)/2
	    
	    # rotate plane and rescale x, y values for this coordinate system
	    deg += 45.0/TILE_WIDTH
	    self.canvas.delete("plane")    # get rid of the old plane before making the new one
	    img = Image.open("Graphics/plane.png")
	    imgRotated = img.rotate(self.planeRotDeg + deg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(startx - x * TILE_WIDTH, starty + y * TILE_HEIGHT, 
	                                          image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	self.planeRotDeg = DIR_SOUTH


    def animateWin(self):
	thread.start_new_thread(self.setOffFireworks, ())


    def killAnimation(self):
	self.animate = False


    def setOffFireworks(self):
	self.animate = True
	x, y = self.canvas.coords("plane")
	self.firework((x-20, y-20), RED1, RED2, RED3)
	self.firework((x+30, y-30), GOLD1, GOLD2, GOLD3)
	self.firework((x, y+20), GREEN1, GREEN2, GREEN3)
	self.firework((x+40, y+20), TURQ1, TURQ2, TURQ3)
	self.firework((x-40, y), PURPLE1, PURPLE2, PURPLE3)
	self.animate = True

    def firework(self, startPos, color1, color2, color3):
	x, y = startPos[0], startPos[1]
	
	if self.animate:
	    l1 = self.canvas.create_line(x, y, x+10, y+10, fill=color1, width=3, smooth=1)
	    l2 = self.canvas.create_line(x+10, y+10, x+20, y, fill=color1, width=3, smooth=1)
	    l3 = self.canvas.create_line(x+11, y+10, x+21, y+10, fill=color1, width=3, smooth=1)
	    l4 = self.canvas.create_line(x+9, y+10, x-1, y+10, fill=color1, width=3, smooth=1)
	    l5 = self.canvas.create_line(x+3, y-3, x+9, y+9, fill=color1, width=3, smooth=1)
	    l6 = self.canvas.create_line(x+17, y-3, x+11, y+9, fill=color1, width=3, smooth=1)
	    l7 = self.canvas.create_line(x+9, y+11, x+1, y+17, fill=color1, width=3, smooth=1)
	    l8 = self.canvas.create_line(x+11, y+11, x+19, y+17, fill=color1, width=3, smooth=1)
	    l9 = self.canvas.create_line(x, y+5, x+9, y+9, fill=color1, width=3, smooth=1)
	    l10 = self.canvas.create_line(x+20, y+5, x+11, y+9, fill=color1, width=3, smooth=1)
	    self.canvas.update()

	    time.sleep(.2)
	    self.canvas.delete(l1)
	    self.canvas.delete(l2)
	    self.canvas.delete(l3)
	    self.canvas.delete(l4)
	    self.canvas.delete(l5)
	    self.canvas.delete(l6)
	    self.canvas.delete(l7)
	    self.canvas.delete(l8)
	    self.canvas.delete(l9)
	    self.canvas.delete(l10)

        if self.animate:
	    l1 = self.canvas.create_line(x-4, y, x+6, y+6, fill=color1, width=3, smooth=1)
	    l2 = self.canvas.create_line(x+14, y+6, x+24, y, fill=color1, width=3, smooth=1)
	    l3 = self.canvas.create_line(x+15, y+10, x+25, y+14, fill=color1, width=3, smooth=1)
	    l4 = self.canvas.create_line(x+5, y+10, x-5, y+14, fill=color1, width=3, smooth=1)
	    l5 = self.canvas.create_line(x-1, y-5, x+5, y+4, fill=color1, width=3, smooth=1)
	    l6 = self.canvas.create_line(x+21, y-5, x+15, y+4, fill=color1, width=3, smooth=1)
	    l7 = self.canvas.create_line(x+5, y+14, x-1, y+22, fill=color1, width=3, smooth=1)
	    l8 = self.canvas.create_line(x+15, y+14, x+21, y+22, fill=color1, width=3, smooth=1)
	    l9 = self.canvas.create_line(x-4, y+5, x+6, y+7, fill=color1, width=3, smooth=1)
	    l10 = self.canvas.create_line(x+24, y+5, x+14, y+7, fill=color1, width=3, smooth=1)
	    self.canvas.update()

	    time.sleep(.2)
	    self.canvas.delete(l1)
	    self.canvas.delete(l2)
	    self.canvas.delete(l3)
	    self.canvas.delete(l4)
	    self.canvas.delete(l5)
	    self.canvas.delete(l6)
	    self.canvas.delete(l7)
	    self.canvas.delete(l8)
	    self.canvas.delete(l9)
	    self.canvas.delete(l10)
        
        if self.animate:
	    l1 = self.canvas.create_line(x-8, y, x+2, y+2, fill=color2, width=2, smooth=1)
	    l2 = self.canvas.create_line(x+18, y+2, x+28, y, fill=color2, width=2, smooth=1)
	    l3 = self.canvas.create_line(x+19, y+12, x+29, y+19, fill=color2, width=2, smooth=1)
	    l4 = self.canvas.create_line(x+1, y+12, x-9, y+19, fill=color2, width=2, smooth=1)
	    l5 = self.canvas.create_line(x-7, y-8, x, y-3, fill=color2, width=2, smooth=1)
	    l6 = self.canvas.create_line(x+27, y-8, x+20, y-3, fill=color2, width=2, smooth=1)
	    l7 = self.canvas.create_line(x+1, y+17, x-3, y+26, fill=color2, width=2, smooth=1)
	    l8 = self.canvas.create_line(x+19, y+17, x+23, y+26, fill=color2, width=2, smooth=1)
	    l9 = self.canvas.create_line(x-8, y+7, x+2, y+5, fill=color2, width=2, smooth=1)
	    l10 = self.canvas.create_line(x+28, y+7, x+18, y+5, fill=color2, width=2, smooth=1)
	    self.canvas.update()

	    time.sleep(.2)
	    self.canvas.delete(l1)
	    self.canvas.delete(l2)
	    self.canvas.delete(l3)
	    self.canvas.delete(l4)
	    self.canvas.delete(l5)
	    self.canvas.delete(l6)
	    self.canvas.delete(l7)
	    self.canvas.delete(l8)
	    self.canvas.delete(l9)
	    self.canvas.delete(l10)
        
        if self.animate:
	    l1 = self.canvas.create_line(x-12, y+2, x-2, y, fill=color2, width=2, smooth=1)
	    l2 = self.canvas.create_line(x+22, y, x+32, y+2, fill=color2, width=2, smooth=1)
	    l3 = self.canvas.create_line(x+22, y+15, x+28, y+23, fill=color2, width=2, smooth=1)
	    l4 = self.canvas.create_line(x-2, y+15, x-8, y+23, fill=color2, width=2, smooth=1)
	    l5 = self.canvas.create_line(x-14, y-10, x-4, y-6, fill=color2, width=2, smooth=1)
	    l6 = self.canvas.create_line(x+34, y-10, x+24, y-6, fill=color2, width=2, smooth=1)
	    l7 = self.canvas.create_line(x-1, y+21, x-4, y+30, fill=color2, width=2, smooth=1)
	    l8 = self.canvas.create_line(x+21, y+21, x+24, y+30, fill=color2, width=2, smooth=1)
	    l9 = self.canvas.create_line(x-12, y+11, x-2, y+7, fill=color2, width=2, smooth=1)
	    l10 = self.canvas.create_line(x+32, y+11, x+22, y+7, fill=color2, width=2, smooth=1)
	    self.canvas.update()

	    time.sleep(.2)
	    self.canvas.delete(l1)
	    self.canvas.delete(l2)
	    self.canvas.delete(l3)
	    self.canvas.delete(l4)
	    self.canvas.delete(l5)
	    self.canvas.delete(l6)
	    self.canvas.delete(l7)
	    self.canvas.delete(l8)
	    self.canvas.delete(l9)
	    self.canvas.delete(l10)
        
        if self.animate:
	    l1 = self.canvas.create_line(x-16, y+5, x-6, y, fill=color3, width=1, smooth=1)
	    l2 = self.canvas.create_line(x+36, y+5, x+26, y, fill=color3, width=1, smooth=1)
	    l3 = self.canvas.create_line(x+25, y+19, x+29, y+28, fill=color3, width=1, smooth=1)
	    l4 = self.canvas.create_line(x-5, y+19, x-9, y+28, fill=color3, width=1, smooth=1)
	    l5 = self.canvas.create_line(x-21, y-12, x-11, y-10, fill=color3, width=1, smooth=1)
	    l6 = self.canvas.create_line(x+41, y-12, x+31, y-10, fill=color3, width=1, smooth=1)
	    l7 = self.canvas.create_line(x-3, y+25, x-5, y+34, fill=color3, width=1, smooth=1)
	    l8 = self.canvas.create_line(x+23, y+25, x+25, y+34, fill=color3, width=1, smooth=1)
	    l9 = self.canvas.create_line(x-16, y+16, x-6, y+9, fill=color3, width=1, smooth=1)
	    l10 = self.canvas.create_line(x+36, y+16, x+26, y+9, fill=color3, width=1, smooth=1)
	    self.canvas.update()

	    time.sleep(.2)
	    self.canvas.delete(l1)
	    self.canvas.delete(l2)
	    self.canvas.delete(l3)
	    self.canvas.delete(l4)
	    self.canvas.delete(l5)
	    self.canvas.delete(l6)
	    self.canvas.delete(l7)
	    self.canvas.delete(l8)
	    self.canvas.delete(l9)
	    self.canvas.delete(l10)
        
        if self.animate:
	    l1 = self.canvas.create_line(x-18, y+8, x-12, y, fill=color3, width=1, smooth=1)
	    l2 = self.canvas.create_line(x+38, y+8, x+32, y, fill=color3, width=1, smooth=1)
	    l3 = self.canvas.create_line(x+28, y+22, x+30, y+32, fill=color3, width=1, smooth=1)
	    l4 = self.canvas.create_line(x-8, y+22, x-10, y+32, fill=color3, width=1, smooth=1)
	    l5 = self.canvas.create_line(x-28, y-13, x-18, y-12, fill=color3, width=1, smooth=1)
	    l6 = self.canvas.create_line(x+48, y-13, x+38, y-12, fill=color3, width=1, smooth=1)
	    l7 = self.canvas.create_line(x-5, y+29, x-6, y+39, fill=color3, width=1, smooth=1)
	    l8 = self.canvas.create_line(x+25, y+29, x+26, y+39, fill=color3, width=1, smooth=1)
	    l9 = self.canvas.create_line(x-19, y+23, x-13, y+13, fill=color3, width=1, smooth=1)
	    l10 = self.canvas.create_line(x+39, y+23, x+33, y+13, fill=color3, width=1, smooth=1)
	    self.canvas.update()
        
	    time.sleep(.2)
	    self.canvas.delete(l1)
	    self.canvas.delete(l2)
	    self.canvas.delete(l3)
	    self.canvas.delete(l4)
	    self.canvas.delete(l5)
	    self.canvas.delete(l6)
	    self.canvas.delete(l7)
	    self.canvas.delete(l8)
	    self.canvas.delete(l9)
	    self.canvas.delete(l10)


    def dropWaterBalloon(self, onKid=False):
	self.numBalloons += 1
	self.animate = True
	thread.start_new_thread(self.waterBalloon, (onKid,))
	
    def waterBalloon(self, onKid):
	# pick a random color
	num = random.randint(1, 6)
	if num == 1:
	    color = "red"
	elif num == 2:
	    color = "orange"
	elif num == 3:
	    color = "yellow"
	elif num == 4:
	    color = "green"
	elif num == 5:
	    color = "blue"
	else:
	    color = "purple"
	string = "Graphics/waterBalloon_" + color

        x, y = self.canvas.coords("plane")
        x = x - 5
        y = y + TILE_HEIGHT

        if self.animate:
	    img = Image.open(string + ".png")
	    nametag = "balloon" + str(self.numBalloons)
	    b = ImageTk.PhotoImage(img)
	    self.canvas.create_image(x, y, image=b, anchor=NW, tag=nametag)
	    self.canvas.update()

        # drop balloon
        if onKid:
	    dist = int(2.6*TILE_HEIGHT)
	else:
	    dist = int(3.1*TILE_HEIGHT)
	
        for i in range(dist):
	    if self.animate:
		time.sleep(.02)
		self.canvas.move(nametag, 0, 1)
		self.canvas.update()

        # set y to new y position
        y = y + dist

        # first stage of bursting
        if self.animate:
	    img = Image.open(string + "2.png")
	    self.canvas.delete(nametag)
	    b = ImageTk.PhotoImage(img)
	    self.canvas.create_image(x, y, image=b, anchor=NW, tag=nametag)
	    self.canvas.update()
	    time.sleep(.17)

        # second stage of bursting
        if self.animate:
	    img = Image.open(string + "3.png")
	    self.canvas.delete(nametag)
	    b = ImageTk.PhotoImage(img)
	    self.canvas.create_image(x, y, image=b, anchor=NW, tag=nametag)
	    self.canvas.update()
	    time.sleep(.17)

        # third stage of bursting
        if self.animate:
	    img = Image.open(string + "4.png")
	    self.canvas.delete(nametag)
	    b = ImageTk.PhotoImage(img)
	    self.canvas.create_image(x, y, image=b, anchor=NW, tag=nametag)
	    self.canvas.update()
	    time.sleep(.17)
        
        # fourth stage of bursting
        if self.animate:
	    img = Image.open(string + "5.png")
	    self.canvas.delete(nametag)
	    b = ImageTk.PhotoImage(img)
	    self.canvas.create_image(x, y, image=b, anchor=NW, tag=nametag)
	    self.canvas.update()
	    time.sleep(.17)
        
        self.balloonList.append(b)


    def askName(self, name, index):
	if self.planeRotDeg == DIR_EAST:
	    self.rotatePlaneClockwise(90)
	else:
	    self.rotatePlaneCounterclockwise(90)
	time.sleep(.3)

	x = TILE_WIDTH*(2.5+index) 
	y = TILE_HEIGHT*7
	y2 = y

	if index % 3 == 1:
	    y2 += 36
	    i = self.bubble1
	elif index % 3 == 2:
	    y2 += 71
	    i = self.bubble2
	else:
	    y2 += 103
	    i = self.bubble3
	
	tag1 = "bubble" + str(self.numNames)
	tag2 = "name" + str(self.numNames)
	self.img = self.canvas.create_image(x, y, image=i, anchor=N, tag=tag1)
	self.text = self.canvas.create_text(x, y2, text=name, font=self.dialogFont, tag=tag2)
	self.canvas.update()
	self.numNames += 1


    def clearNames(self):
	for i in range(0, self.numNames):
	    tag1 = "bubble" + str(i)
	    tag2 = "name" + str(i)
	    self.canvas.delete(tag1)
	    self.canvas.delete(tag2)
	self.numNames = 0

    def crash(self):
	x, y = self.canvas.coords("plane")
	for i in range(1, 11):
	    img = Image.open("Graphics/planeFade" + str(i) + ".png")
	    imgRotated = img.rotate(self.planeRotDeg)
	    self.planeImg = ImageTk.PhotoImage(imgRotated)
	    self.plane = self.canvas.create_image(x, y, image=self.planeImg, anchor=NW, tags="plane")
	    self.canvas.update()
	    time.sleep(.17)
	self.canvas.delete("plane")