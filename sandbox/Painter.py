#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from PIL import Image, ImageTk
import time
import cmath, math
import tkFont

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

class Painter:

    def __init__(self, canvas, charArray):

        self.canvas = canvas
        self.paintMap(charArray)
        
        self.waitingOutline = self.canvas.create_rectangle(460, 90, 720, 130, fill="Yellow",
                                                           dash='3', width=2, state=HIDDEN)
        self.waitingText = self.canvas.create_text(588, 110, font=tkFont.Font(family="Pupcat", size=20, 
	                                           weight=tkFont.BOLD), text="Checking your code...", state=HIDDEN)

        self.firework((550, 350), 'red')
        self.firework((600, 300), 'blue')

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

        img_goal = Image.open("Graphics/Tiles/goal.png")

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

        self.goal = ImageTk.PhotoImage(img_goal)

        for row in range(0, NUM_TILES_HIGH):

            for col in range(0, NUM_TILES_WIDE):

                x = col*TILE_WIDTH
                y = row*TILE_HEIGHT

                # air
                if charArray[row][col] == 'A':
                    self.canvas.create_image(x, y, image=self.air, anchor=NW)

                # cloud wall
                elif charArray[row][col] == 'W':
                    self.canvas.create_image(x, y, image=(self.makeWall(charArray, row, col)), anchor=NW)

                # cloud island
                elif charArray[row][col] == 'I':
                    self.canvas.create_image(x, y, image=(self.makeIsland(charArray, row, col)), anchor=NW)

                # goal 
                elif charArray[row][col] == 'G':
                    self.canvas.create_image(x, y, image=self.goal, anchor=NW)

                # plane - set plane here and make square underneath air
                elif charArray[row][col] == 'P':
		    self.canvas.create_image(x, y, image=self.air, anchor=NW)
		    self.planeX = x
		    self.planeY = y

                else:
                    print "Unrecognized character ", charArray[row][col], " in map file."
                    self.canvas.create_image(x, y, image=self.air, anchor=NW)

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
	    time.sleep(.025)
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
	    time.sleep(.025)
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

	for i in range(0, TILE_WIDTH):
	    time.sleep(.025)
	    self.canvas.move("plane", 0, -1)
	    self.canvas.update()


    def movePlaneSouth(self):
	# make sure we're facing in the correct direction first
	if self.planeRotDeg != DIR_SOUTH:
	    if self.planeRotDeg == DIR_EAST:   # turn counterclockwise
	        self.rotatePlaneCounterclockwise(90)
	    else:       # turn clockwise
		self.rotatePlaneClockwise(abs(self.planeRotDeg - DIR_SOUTH))
	self.planeRotDeg = DIR_SOUTH

	for i in range(0, TILE_WIDTH):
	    time.sleep(.025)
	    self.canvas.move("plane", 0, 1)
	    self.canvas.update()


    def rotatePlaneClockwise(self, numDegrees):
	x, y = self.canvas.coords("plane")
	for deg in range(0, numDegrees):
	    time.sleep(.012)
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
	    time.sleep(.012)
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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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
	    time.sleep(.025)

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


    def firework(self, startPos, color):
	x, y = startPos[0], startPos[1]
	
	l1 = self.canvas.create_line(x, y, x+10, y+10, fill=color, width=3, smooth=1)
	l2 = self.canvas.create_line(x+10, y+10, x+20, y, fill=color, width=3, smooth=1)
	l3 = self.canvas.create_line(x+11, y+10, x+21, y+10, fill=color, width=3, smooth=1)
	l4 = self.canvas.create_line(x+9, y+10, x-1, y+10, fill=color, width=3, smooth=1)
        self.canvas.update()

        time.sleep(.5)
        self.canvas.delete(l1)
        self.canvas.delete(l2)
        self.canvas.delete(l3)
        self.canvas.delete(l4)
        l1 = self.canvas.create_line(x-4, y, x+6, y+6, fill=color, width=3, smooth=1)
        l2 = self.canvas.create_line(x+14, y+6, x+24, y, fill=color, width=3, smooth=1)
        l3 = self.canvas.create_line(x+15, y+10, x+25, y+14, fill=color, width=3, smooth=1)
        l4 = self.canvas.create_line(x+5, y+10, x-5, y+14, fill=color, width=3, smooth=1)
        self.canvas.update()

        time.sleep(.5)
        self.canvas.delete(l1)
        self.canvas.delete(l2)
        self.canvas.delete(l3)
        self.canvas.delete(l4)
        l1 = self.canvas.create_line(x-8, y, x+2, y+2, fill=color, width=3, smooth=1)
        l2 = self.canvas.create_line(x+18, y+2, x+28, y, fill=color, width=3, smooth=1)
        l3 = self.canvas.create_line(x+19, y+12, x+29, y+19, fill=color, width=3, smooth=1)
        l4 = self.canvas.create_line(x+1, y+12, x-9, y+19, fill=color, width=3, smooth=1)
        self.canvas.update()

        time.sleep(.5)
        self.canvas.delete(l1)
        self.canvas.delete(l2)
        self.canvas.delete(l3)
        self.canvas.delete(l4)
        l1 = self.canvas.create_line(x-12, y, x-2, y, fill=color, width=3, smooth=1)
        l2 = self.canvas.create_line(x+22, y, x+32, y, fill=color, width=3, smooth=1)
        l3 = self.canvas.create_line(x+23, y+13, x+28, y+23, fill=color, width=3, smooth=1)
        l4 = self.canvas.create_line(x-3, y+13, x-8, y+23, fill=color, width=3, smooth=1)
        self.canvas.update()

        time.sleep(.5)
        self.canvas.delete(l1)
        self.canvas.delete(l2)
        self.canvas.delete(l3)
        self.canvas.delete(l4)
        l1 = self.canvas.create_line(x-16, y+3, x-6, y-2, fill=color, width=3, smooth=1)
        l2 = self.canvas.create_line(x+36, y+3, x+26, y-2, fill=color, width=3, smooth=1)
        l3 = self.canvas.create_line(x+28, y+15, x+29, y+24, fill=color, width=3, smooth=1)
        l4 = self.canvas.create_line(x-8, y+15, x-9, y+24, fill=color, width=3, smooth=1)
        self.canvas.update()

        time.sleep(.5)
        self.canvas.delete(l1)
        self.canvas.delete(l2)
        self.canvas.delete(l3)
        self.canvas.delete(l4)
        l1 = self.canvas.create_line(x-18, y+8, x-12, y, fill=color, width=3, smooth=1)
        l2 = self.canvas.create_line(x+38, y+8, x+32, y, fill=color, width=3, smooth=1)
        l3 = self.canvas.create_line(x+28, y+18, x+29, y+27, fill=color, width=3, smooth=1)
        l4 = self.canvas.create_line(x-8, y+18, x-9, y+27, fill=color, width=3, smooth=1)
        
        time.sleep(.5)
        self.canvas.delete(l1)
        self.canvas.delete(l2)
        self.canvas.delete(l3)
        self.canvas.delete(l4)